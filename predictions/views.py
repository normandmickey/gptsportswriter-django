import re, os, praw, requests, pytz
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime
from .chat_completion import generate_prediction
from .image_generation import generate_image
from praw.models import InlineImage
from dotenv import load_dotenv
from datetime import datetime as dtdt

load_dotenv()

ODDSAPI_API_KEY=os.environ.get("ODDSAPI_API_KEY")

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

def getGames():
    sports = ['baseball_mlb','soccer_usa_mls','basketball_nba','icehockey_nhl','soccer_epl','soccer_spain_la_liga']
    
    dataGames = []
    for sport in sports:
        dataMatch = requests.get(f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDSAPI_API_KEY}&regions=us&markets=h2h&bookmakers=draftkings,fanduel")
        dataMatch = dataMatch.json()
        for i in range(len(dataMatch)):
            try:
                t = dataMatch[i]['commence_time']
            except:
                t = "2024-02-25 12:00:00-05:00"
            utcTime = dtdt(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19]), tzinfo=utc)
            esTime = utcTime.astimezone(ept)
            dataGames.append(dataMatch[i]['sport_key'] + " - " + dataMatch[i]['away_team'] + " VS " + dataMatch[i]['home_team'] + " Prediction " + str(esTime))

    for sport in sports:
        dataResults = requests.get(f"https://api.the-odds-api.com/v4/sports/{sport}/scores/?daysFrom=1&apiKey={ODDSAPI_API_KEY}")
        dataResults = dataResults.json()
        try:
            for i in range(len(dataResults)):
                if dataResults[i]['completed']:
                    t = dataResults[i]['commence_time']
                    utcTime = dtdt(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19]), tzinfo=utc)
                    esTime = utcTime.astimezone(ept)
                    dataGames.append(dataResults[i]['sport_key'] + " - " + dataResults[i]['home_team'] + " VS " + dataResults[i]['away_team'] + " Recap " + str(esTime)) 
                else:
                    print("error")      
        except:
            print("error")
        
        
    #print(dataGames)
    return(dataGames)

# Create your views here.
def home(request):
    return render(request, "predictions/home.html")

def about(request):
    return render(request, "predictions/about.html")

def predictions(request):
    context = {}
    user_input = ""
   
    if request.method == "GET":
        dataGames = getGames()
        print(dataGames)
        return render(request, "predictions/predictions.html", {'games': dataGames})
    else:
        if "game" in request.POST:
            user_input += request.POST.get("game") + "\n"

        generated_prediction = generate_prediction(user_input)
        image_prompt = (
            f"Generate an image that visually illustrates the essence of the following story: {generated_prediction}"
        )
        image_url = generate_image(image_prompt)
        print(image_url)
        data = requests.get(image_url).content
        f = open('img.jpg', 'wb')
        f.write(data)
        f.close

        
        context = {
            "user_input": user_input,
            "generated_prediction": generated_prediction.replace("\n", "<br/>"),
            "image_url": image_url,
        }

        title = user_input
        image = InlineImage(path="img.jpg", caption=title)
        media = {"image1": image}
        selfText = "{image1}" + generated_prediction
        try:
            subreddit.submit(title, inline_media=media, selftext=selfText)
        except:
            print("error submitting reddit post")
        
        return render(request, "predictions/predictions.html", context)