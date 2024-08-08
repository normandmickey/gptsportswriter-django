import re, os, praw, requests, pytz, time, json
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime
from .chat_completion import generate_prediction, generate_recap, generate_tweet, generate_parlay, generate_news, generate_videoText, generate_prop
from .image_generation import generate_image, createImagePrompt
from praw.models import InlineImage
from dotenv import load_dotenv
from datetime import datetime as dtdt
from django.http import JsonResponse
import facebook as fb
import tweepy
import openai

load_dotenv()

ODDSAPI_API_KEY=os.environ.get("ODDSAPI_API_KEY")
consumer_key=os.environ.get('TWITTER_API_KEY')
consumer_secret=os.environ.get('TWITTER_API_SECRET')
bearer_token=os.environ.get('TWITTER_BEARER_TOKEN')
access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
access_token=os.environ.get('TWITTER_ACCESS_TOKEN')

ept = pytz.timezone('US/Eastern')
utc = pytz.utc
# str format
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent="GPTSportsWriter by u/GPTSportsWriter",
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD")
)

subreddit = reddit.subreddit("gptsportswriter")

tweepy_auth = tweepy.OAuth1UserHandler(
    "{}".format(os.environ.get("TWITTER_API_KEY")),
    "{}".format(os.environ.get("TWITTER_API_SECRET")),
    "{}".format(os.environ.get("TWITTER_ACCESS_TOKEN")),
    "{}".format(os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")),
)

# send Tweet
def sendTweet(text, redditURL):
    tweetText = createTweet(text)
    tweetText = tweetText[:270]
    #tweetText = tweetText + " " + redditURL
    print(tweetText)
    tweepy_api = tweepy.API(tweepy_auth)
    post = tweepy_api.simple_upload("img.jpg")
    text = str(post)
    media_id = re.search("media_id=(.+?),", text).group(1)
    
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Post Tweet
    response = client.create_tweet(text=tweetText, media_ids=[media_id])
    #print(response)

def openAITTS(text):
    speech_file_path = "speech.mp3"
    response = openai.audio.speech.create(
        model="tts-1",
        voice="echo",
        speed=1,
        input=text
        )
    response.stream_to_file(speech_file_path)

def createTweet(text):
    tweetText = generate_tweet(text)
    tweetText = tweetText.replace('"', '')
    tweetText = tweetText
    return(tweetText)

def fbPost(text, title):
    postBody = title + "\n" + text
    gptsportswriterapi=fb.GraphAPI(os.environ.get('FACEBOOK_ACCESS_TOKEN'))
    response_photo = gptsportswriterapi.put_photo(open('img.jpg','rb'), message=postBody)
    #print(response_photo)
    #photoJson = json.loads(response_photo)
    #photo_id = photoJson[0]['id']
    #gptsportswriterapi.put_object(parent_object="me",connection_name="feed",message=text,link="https://www.gptsportswriter.com",photo_id=photo_id)
    #print(photo_id)

def getSports():
    sports = []
    sport = requests.get(f"https://api.the-odds-api.com/v4/sports/?apiKey={ODDSAPI_API_KEY}")
    sport = sport.json()
    for i in range(len(sport)):
        if sport[i]['has_outrights'] == False:
            sports.append(sport[i]['key'])
            #print(sport[i]['key'])
    return(sports)

def getLeagues():
    leagues = []
    sport = requests.get(f"https://api.the-odds-api.com/v4/sports/?apiKey={ODDSAPI_API_KEY}")
    sport = sport.json()
    for i in range(len(sport)):
        if sport[i]['has_outrights'] == False:
            leagues.append(sport[i]['description'])
            #print(sport[i]['key'])
    leagues = [i for n, i in enumerate(leagues) if i not in leagues[:n]]
    return(leagues)
            
def ajax_handler(request,sport):
    games = []
    dataMatch = requests.get(f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDSAPI_API_KEY}&regions=us&markets=h2h&bookmakers=draftkings,fanduel")
    dataMatch = dataMatch.json()
    #print("predictions: " + str(dataMatch))
    for i in range(len(dataMatch)):
        try:
            t = dataMatch[i]['commence_time']
        except:
            t = "2024-02-25 12:00:00-05:00"
        utcTime = dtdt(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19]), tzinfo=utc)
        esTime = utcTime.astimezone(ept)
        games.append(dataMatch[i]['id'] + ": " + dataMatch[i]['away_team'] + " VS " + dataMatch[i]['home_team'] + " " + str(esTime))
        
    return JsonResponse({'games': games})

def ajax_handlerb(request,sport):
    games = []
    dataMatch = requests.get(f"https://api.the-odds-api.com/v4/sports/{sport}/scores/?apiKey={ODDSAPI_API_KEY}&daysFrom=2")
    dataMatch = dataMatch.json()
    #print("recaps: " + str(dataMatch))
    for i in range(len(dataMatch)):
        try:
            t = dataMatch[i]['commence_time']
        except:
            t = "2024-02-25 12:00:00-05:00"
        utcTime = dtdt(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19]), tzinfo=utc)
        esTime = utcTime.astimezone(ept)
        if dataMatch[i]['completed'] == True:
            games.append(dataMatch[i]['id'] + ": " + dataMatch[i]['away_team'] + " VS " + dataMatch[i]['home_team'] + " " + str(esTime))
        
    return JsonResponse({'games': games})


# Create your views here.
def home(request):
    return render(request, "predictions/home.html")

def about(request):
    return render(request, "predictions/about.html")

def fbprivacy(request):
    return render(request, "predictions/fbprivacy.html")

def parlays(request):
    context = {}
    user_input = ""
    sportKey = ""
    sport = ""
    sports = getSports()
    
    if request.method == "GET":
        dataSports = getSports()
        return render(request, "predictions/parlays.html", {'sports': dataSports})
    else:
        if "game" in request.POST:
            user_input += request.POST.get("game") + "\n"
            gameSplit = user_input.split(':')
            gameId=gameSplit[0]
            match=gameSplit[1]
            sportKey += request.POST.get("sport")
            sport += request.POST.get("sport") + "\n"
            sport = sport.replace('_', " ")
        
        generated_parlay = generate_parlay(sport + " " + match, gameId, sportKey)
        image_prompt = createImagePrompt(sport + " " + match)
        #print(image_prompt)
        image_url = generate_image(image_prompt)
        #print(image_url)
        time.sleep(2)
        data = requests.get(image_url).content
        f = open('img.jpg', 'wb')
        f.write(data)
        f.close
            
        context = {
            "user_input": match,
            "generated_parlay": generated_parlay.replace("\n", "<br/>"),
            "image_url": image_url,
            "sports": sports,
        }

        title = "Parlay: " + match
        image = InlineImage(path="img.jpg", caption=title)
        media = {"image1": image}
        selfText = "{image1}" + generated_parlay
        try:
            redditURL = subreddit.submit(title, inline_media=media, selftext=selfText)
            redditURL = "https://redd.it/" + str(redditURL)
            #print(redditURL)
        except:
            print("error submitting reddit post")
        
        try:
            sendTweet(generated_parlay, redditURL)
        except:
            print("error sending tweet")

        try:
            fbPost(generated_parlay, match)
        except:
            print("error posting to FB")
        
        return render(request, "predictions/parlays.html", context)

def topnews(request):
    context = {}
    user_input = ""
    sport = ""
    #sports = getLeagues()
    sports = ['Baseball MLB','Basketball NCAA','Basketball NBA','Football NCAA','Football NFL','Golf PGA','Ice Hockey NHL','Soccer MLS','Soccer EPL','Tennis','Summer Olypmics 2024','2034 Winter Olympics','Olympic Breakdancing','Olympic Badminton','Olympic Soccer','Olympic Rowing','Olympic Basketball','Olympic Fencing','Olympic Judo','Olympic Rowing','Olympic Gymnastics','Olympic Diving','Olympic Swimming','Olympic Tennis','Olympic Surfing','Olympic Handball','Olympic Wrestling','Olympic Table Tennis','Olympic Volleyball','Olympic Water Polo','Olympic Track','NASCAR Cup Series','Team USA Olympics']
    
    if request.method == "GET":
        #dataSports = getLeagues()
        dataSports = sports
        return render(request, "predictions/topnews.html", {'sports': dataSports})
    else:
        if "sport" in request.POST:
            user_input += request.POST.get("sport") + "\n"
            sport += request.POST.get("sport") + "\n"
            sport = sport.replace('_', " ")
            res = re.split('\s+', user_input)
            print(res)
        
        print("sport: " + sport)
        generated_news = generate_news(sport, res)
        image_prompt = createImagePrompt(sport)
        #print(image_prompt)
        image_url = generate_image(image_prompt)
        #print(image_url)
        time.sleep(2)
        data = requests.get(image_url).content
        f = open('img.jpg', 'wb')
        f.write(data)
        f.close
            
        context = {
            "user_input": user_input,
            "generated_news": generated_news.replace("\n", "<br/>"),
            "image_url": image_url,
            "sports": sports,
        }

        title = "Top News: " + user_input
        image = InlineImage(path="img.jpg", caption=title)
        media = {"image1": image}
        selfText = "{image1}" + generated_news
        try:
            redditURL = subreddit.submit(title, inline_media=media, selftext=selfText)
            redditURL = "https://redd.it/" + str(redditURL)
            #print(redditURL)
        except:
            print("error submitting reddit post")
        
        try:
            sendTweet(generated_news, redditURL)
        except:
            print("error sending tweet")

        try:
            fbPost(generated_news, user_input)
        except:
            print("error posting to FB")
        
        return render(request, "predictions/topnews.html", context)

def predictions(request):
    context = {}
    user_input = ""
    sportKey = ""
    sport = ""
    sports = getSports()
    
    if request.method == "GET":
        dataSports = getSports()
        return render(request, "predictions/predictions.html", {'sports': dataSports})
    else:
        if "game" in request.POST:
            user_input += request.POST.get("game") + "\n"
            gameSplit = user_input.split(':')
            gameId=gameSplit[0]
            match=gameSplit[1]
            sportKey += request.POST.get("sport")
            sport += request.POST.get("sport") + "\n"
            sport = sport.replace('_', " ")
            res = re.split('\s+', match)
            res.remove('VS')
            res = res[:len(res)-3]
            print(res)
                           
        generated_prediction = generate_prediction(sport + " " + match, res, gameId, sportKey)
        image_prompt = createImagePrompt(sport + " " + match)
        #print(image_prompt)
        image_url = generate_image(image_prompt)
        #print(image_url)
        time.sleep(2)
        data = requests.get(image_url).content
        f = open('img.jpg', 'wb')
        f.write(data)
        f.close
            
        context = {
            "user_input": match,
            "generated_prediction": generated_prediction.replace("\n", "<br/>"),
            "image_url": image_url,
            "sports": sports,
        }

        title = "Prediction: " + match
        image = InlineImage(path="img.jpg", caption=title)
        media = {"image1": image}
        selfText = "{image1}" + generated_prediction
        #videoText = generate_videoText(generated_prediction)
        #openAITTS(videoText)
        try:
            redditURL = subreddit.submit(title, inline_media=media, selftext=selfText)
            redditURL = "https://redd.it/" + str(redditURL)
            #print(redditURL)
        except:
            print("error submitting reddit post")
        
        try:
            sendTweet(generated_prediction, redditURL)
        except:
            print("error sending tweet")

        try:
            fbPost(generated_prediction, match)
        except:
            print("error posting to FB")
        
        return render(request, "predictions/predictions.html", context)

def props(request):
    context = {}
    user_input = ""
    sportKey = ""
    sport = ""
    sports = getSports()
    
    if request.method == "GET":
        dataSports = getSports()
        return render(request, "predictions/props.html", {'sports': dataSports})
    else:
        if "game" in request.POST:
            user_input += request.POST.get("game") + "\n"
            gameSplit = user_input.split(':')
            gameId=gameSplit[0]
            match=gameSplit[1]
            sportKey += request.POST.get("sport")
            sport += request.POST.get("sport") + "\n"
            sport = sport.replace('_', " ")
            res = re.split('\s+', match)
            res.remove('VS')
            res = res[:len(res)-3]
            print(res)
                           
        generated_prop = generate_prop(sport + " " + match, res, gameId, sportKey)
        image_prompt = createImagePrompt(sport + " " + match)
        #print(image_prompt)
        image_url = generate_image(image_prompt)
        #print(image_url)
        time.sleep(2)
        data = requests.get(image_url).content
        f = open('img.jpg', 'wb')
        f.write(data)
        f.close
            
        context = {
            "user_input": match,
            "generated_prediction": generated_prop.replace("\n", "<br/>"),
            "image_url": image_url,
            "sports": sports,
        }

        title = "Prediction: " + match
        image = InlineImage(path="img.jpg", caption=title)
        media = {"image1": image}
        selfText = "{image1}" + generated_prop
        #videoText = generate_videoText(generated_prediction)
        #openAITTS(videoText)
        try:
            redditURL = subreddit.submit(title, inline_media=media, selftext=selfText)
            redditURL = "https://redd.it/" + str(redditURL)
            #print(redditURL)
        except:
            print("error submitting reddit post")
        
        try:
            sendTweet(generated_prop, redditURL)
        except:
            print("error sending tweet")

        try:
            fbPost(generated_prop, match)
        except:
            print("error posting to FB")
        
        return render(request, "predictions/props.html", context)


def recaps(request):
    context = {}
    user_input = ""
    sportKey = ""
    sports = getSports()
    sport = ""
    
    if request.method == "GET":
        dataSports = getSports()
        return render(request, "predictions/recaps.html", {'sports': dataSports})
    else:
        if "game" in request.POST:
            user_input += request.POST.get("game") + "\n"
            gameSplit = user_input.split(':')
            gameId=gameSplit[0]
            match=gameSplit[1]
            sportKey += request.POST.get("sport")
            sport += request.POST.get("sport") + "\n"
            sport = sport.replace('_', " ")
            res = re.split('\s+', match)
            res.remove('VS')
            res = res[:len(res)-3]
            
        
        generated_recap = generate_recap(sport + " " + match, res, gameId, sportKey)
        image_prompt = createImagePrompt(sport + " " + match)
        #print(image_prompt)
        image_url = generate_image(image_prompt)
        #print(image_url)
        time.sleep(2)
        data = requests.get(image_url).content
        f = open('img.jpg', 'wb')
        f.write(data)
        f.close
            
        context = {
            "user_input": match,
            "generated_recap": generated_recap.replace("\n", "<br/>"),
            "image_url": image_url,
            "sports": sports,
        }

        title = "Recap: " + match
        image = InlineImage(path="img.jpg", caption=title)
        media = {"image1": image}
        selfText = "{image1}" + generated_recap
        try:
            #subreddit.submit(title, inline_media=media, selftext=selfText)
            redditURL = subreddit.submit(title, inline_media=media, selftext=selfText)
            redditURL = "https://redd.it/" + str(redditURL)
        except:
            print("error submitting reddit post")

        try:
            sendTweet(generated_recap, redditURL)
        except:
            print("error sending tweet")

        try:
            fbPost(generated_recap, match)
        except:
            print("error posting to FB")
        
        return render(request, "predictions/recaps.html", context)