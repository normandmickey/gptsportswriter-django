import re, os, praw, requests
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime
from .chat_completion import generate_prediction
from .image_generation import generate_image
from praw.models import InlineImage
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent="GPTSportsWriter by u/GPTSportsWriter",
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD")
)

subreddit = reddit.subreddit("gptsportswriter")

# Create your views here.
def home(request):
    return render(request, "predictions/home.html")

def about(request):
    return render(request, "predictions/about.html")

def predictions(request):
    context = {}
    user_input = ""
    if request.method == "GET":
        return render(request, "predictions/predictions.html")
    else:
        if "text_input" in request.POST:
            user_input += request.POST.get("text_input") + "\n"

        generated_prediction = generate_prediction(user_input)
        image_prompt = (
            f"Generate an image that visually illustrates the essence of the following story: {generated_prediction}"
        )
        image_url = generate_image(image_prompt)
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