from django.urls import path
from predictions import views

urlpatterns = [
    path("", views.home, name="home"),
    path('recent-predictions/', views.recent_predictions, name='recent_predictions'),
    path('recent-parlays/', views.recent_parlays, name='recent_parlays'),
    path('recent-recaps/', views.recent_recaps, name='recent_recaps'),
    path('recent-props/', views.recent_props, name='recent_props'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
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