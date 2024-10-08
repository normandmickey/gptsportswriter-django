from django.urls import path
from predictions import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("fbprivacy/", views.fbprivacy, name="fbprivacy"),
    path("discordTOS/", views.discordTOS, name="discordTOS"),
    path("discordPrivacy/", views.discordPrivacy, name="discordPrivacy"),
    path("predictions/", views.predictions, name="predictions"),
    path("recaps/", views.recaps, name="recaps"),
    path("parlays/", views.parlays, name="parlays"),
    path("topnews/", views.topnews, name="topnews"),
    path("props/", views.props, name="props"),
    path('ajax_handler/<str:sport>',views.ajax_handler,name="ajax_handler"),
    path('ajax_handlerb/<str:sport>',views.ajax_handlerb,name="ajax_handlerb")
]