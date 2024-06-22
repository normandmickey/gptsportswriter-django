from django.urls import path
from predictions import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("predictions/", views.predictions, name="predictions"),
]