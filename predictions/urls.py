from django.urls import path
from predictions import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("fbprivacy/", views.fbprivacy, name="fbprivacy"),
    path("discordTOS/", views.discordTOS, name="discordTOS"),
    path("discordPrivacy/", views.discordPrivacy, name="discordPrivacy"),
    path("zoomPrivacy/", views.zoomPrivacy, name="zoomPrivacy"),
    path("zoom-tos/", views.zoomTOS, name="zoomTOS"),
    path("zoom-privacy/", views.zoomPrivacy, name="zoomPrivacy"),
    path("zoom-support/", views.zoomSupport, name="zoomTOS"),
    path("zoom-documentation/", views.zoomDocumentation, name="zoomPrivacy"),
    path("predictions/", views.predictions, name="predictions"),
    path("recaps/", views.recaps, name="recaps"),
    path("parlays/", views.parlays, name="parlays"),
    path("topnews/", views.topnews, name="topnews"),
    path("props/", views.props, name="props"),
    path('ajax_handler/<str:sport>',views.ajax_handler,name="ajax_handler"),
    path('ajax_handlerb/<str:sport>',views.ajax_handlerb,name="ajax_handlerb")
]