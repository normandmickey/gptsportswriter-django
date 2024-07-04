from django.urls import path
from predictions import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
     path("fbprivacy/", views.fbprivacy, name="fbprivacy"),
    path("predictions/", views.predictions, name="predictions"),
    path("recaps/", views.recaps, name="recaps"),
    path('ajax_handler/<str:sport>',views.ajax_handler,name="ajax_handler"),
    path('ajax_handlerb/<str:sport>',views.ajax_handlerb,name="ajax_handlerb")
]