import re
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import datetime
from .chat_completion import generate_prediction


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
        
        context = {
            "user_input": user_input,
            "generated_prediction": generated_prediction.replace("\n", "<br/>"),
        }

        return render(request, "predictions/predictions.html", context)