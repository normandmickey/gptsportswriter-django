from django.urls import path
from predictions import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("predictions/", views.predictions, name="predictions"),
    path('ajax_handler/<str:sport>',views.ajax_handler,name="ajax_handler")
]