import re, os, praw, requests, pytz, time
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime
from .chat_completion import generate_prediction, generate_recap, generate_tweet
from .image_generation import generate_image, createImagePrompt
from praw.models import InlineImage
from dotenv import load_dotenv
from datetime import datetime as dtdt
from django.http import JsonResponse
import tweepy

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

# send Tweet
def sendTweet(text,redditURL):
    tweetText = createTweet(text,redditURL)
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Post Tweet
    response = client.create_tweet(text=tweetText)
    print(response)

def createTweet(text, redditURL):
    tweetText = generate_tweet(text)
    tweetText = tweetText.replace('"', '')
    return(tweetText)


def getSports():
    sports = []
    sport = requests.get(f"https://api.the-odds-api.com/v4/sports/?apiKey={ODDSAPI_API_KEY}")
    sport = sport.json()
    for i in range(len(sport)):
        if sport[i]['has_outrights'] == False:
            sports.append(sport[i]['key'])
    return(sports)
            
def ajax_handler(request,sport):
    games = []
    dataMatch = requests.get(f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDSAPI_API_KEY}&regions=us&markets=h2h&bookmakers=draftkings,fanduel")
    dataMatch = dataMatch.json()
    print("predictions: " + str(dataMatch))
    for i in range(len(dataMatch)):
        try:
            t = dataMatch[i]['commence_time']
        except:
            t = "2024-02-25 12:00:00-05:00"
        utcTime = dtdt(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19]), tzinfo=utc)
        esTime = utcTime.astimezone(ept)
        games.append(dataMatch[i]['away_team'] + " VS " + dataMatch[i]['home_team'] + " " + str(esTime))
        
    return JsonResponse({'games': games})

def ajax_handlerb(request,sport):
    games = []
    dataMatch = requests.get(f"https://api.the-odds-api.com/v4/sports/{sport}/scores/?apiKey={ODDSAPI_API_KEY}&daysFrom=3")
    dataMatch = dataMatch.json()
    print("recaps: " + str(dataMatch))
    for i in range(len(dataMatch)):
        try:
            t = dataMatch[i]['commence_time']
        except:
            t = "2024-02-25 12:00:00-05:00"
        utcTime = dtdt(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19]), tzinfo=utc)
        esTime = utcTime.astimezone(ept)
        if dataMatch[i]['completed'] == True:
            games.append(dataMatch[i]['away_team'] + " VS " + dataMatch[i]['home_team'] + " " + str(esTime))
        
    return JsonResponse({'games': games})


# Create your views here.
def home(request):
    return render(request, "predictions/home.html")

def about(request):
    return render(request, "predictions/about.html")

def predictions(request):
    context = {}
    user_input = ""
    sports = getSports()
    
    if request.method == "GET":
        dataSports = getSports()
        return render(request, "predictions/predictions.html", {'sports': dataSports})
    else:
        if "game" in request.POST:
            user_input += request.POST.get("game") + "\n"
        
        generated_prediction = generate_prediction(user_input)
        image_prompt = createImagePrompt(user_input)
        print(image_prompt)
        image_url = generate_image(image_prompt)
        print(image_url)
        time.sleep(2)
        data = requests.get(image_url).content
        f = open('img.jpg', 'wb')
        f.write(data)
        f.close
            
        context = {
            "user_input": user_input,
            "generated_prediction": generated_prediction.replace("\n", "<br/>"),
            "image_url": image_url,
            "sports": sports,
        }

        title = "Prediction: " + user_input
        image = InlineImage(path="img.jpg", caption=title)
        media = {"image1": image}
        selfText = "{image1}" + generated_prediction
        try:
            redditURL = subreddit.submit(title, inline_media=media, selftext=selfText)
            sendTweet(user_input,redditURL)
        except:
            print("error submitting reddit post")
        
        return render(request, "predictions/predictions.html", context)

def recaps(request):
    context = {}
    user_input = ""
    sports = getSports()
    
    if request.method == "GET":
        dataSports = getSports()
        return render(request, "predictions/recaps.html", {'sports': dataSports})
    else:
        if "game" in request.POST:
            user_input += request.POST.get("game") + "\n"
        
        generated_recap = generate_recap(user_input)
        image_prompt = createImagePrompt(user_input)
        print(image_prompt)
        image_url = generate_image(image_prompt)
        print(image_url)
        time.sleep(2)
        data = requests.get(image_url).content
        f = open('img.jpg', 'wb')
        f.write(data)
        f.close
            
        context = {
            "user_input": user_input,
            "generated_recap": generated_recap.replace("\n", "<br/>"),
            "image_url": image_url,
            "sports": sports,
        }

        title = "Recap: " + user_input
        image = InlineImage(path="img.jpg", caption=title)
        media = {"image1": image}
        selfText = "{image1}" + generated_recap
        try:
            subreddit.submit(title, inline_media=media, selftext=selfText)
        except:
            print("error submitting reddit post")
        
        return render(request, "predictions/recaps.html", context)