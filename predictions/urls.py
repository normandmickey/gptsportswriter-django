from django.urls import path
from predictions import views
from django.contrib.sitemaps import GenericSitemap 
from django.contrib.sitemaps.views import sitemap
from .models import Predictions, Recaps, Parlays, Props
from django.urls import path, include
from itertools import chain
from django.views.generic.base import TemplateView


# new dict below...
info_dict = {
    "queryset": Predictions.objects.all().defer('gameimg').order_by('created_at'),
    "date_field": "updated_at",
}

# new dict below...
info_dict2 = {
    "queryset": Parlays.objects.all().defer('gameimg').order_by('created_at'),
    "date_field": "updated_at",
}

# new dict below...
info_dict3 = {
    "queryset": Props.objects.all().defer('gameimg').order_by('created_at'),
    "date_field": "updated_at",
}

# new dict below...
info_dict4 = {
    "queryset": Recaps.objects.all().defer('gameimg').order_by('created_at'),
    "date_field": "updated_at",
}

urlpatterns = [
    path("", views.home, name="home"),
    path('c41a1070cbfa4d5ea66773fc0519716c.txt', TemplateView.as_view(template_name='c41a1070cbfa4d5ea66773fc0519716c.txt',
                                      content_type='text/plain')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt',
                                      content_type='text/plain')),
    path('current-odds/', views.current_odds, name='current_odds'),
    path('recent-predictions/', views.recent_predictions, name='recent_predictions'),
    path('prediction-results/', views.prediction_results, name='prediction_results'),
    path('current-odds/', views.current_odds, name='current_odds'),
    path('odds/', views.odds, name='odds'),
    path('recent-parlays/', views.recent_parlays, name='recent_parlays'),
    path('recent-recaps/', views.recent_recaps, name='recent_recaps'),
    path('recent-props/', views.recent_props, name='recent_props'),
    path('prediction-detail/<slug:slug>/', views.prediction_detail, name='prediction_detail'),
    path('article-detail/<slug:slug>/', views.article_detail, name='article_detail'),
    path('recap-detail/<slug:slug>/', views.recap_detail, name='recap_detail'),
    path('prop-detail/<slug:slug>/', views.prop_detail, name='prop_detail'),
    path('parlay-detail/<slug:slug>/', views.parlay_detail, name='parlay_detail'),
    path("about/", views.about, name="about"),
    path("fbprivacy/", views.fbprivacy, name="fbprivacy"),
    path("discordTOS/", views.discordTOS, name="discordTOS"),
    path("discordPrivacy/", views.discordPrivacy, name="discordPrivacy"),
    path("zoomPrivacy/", views.zoomPrivacy, name="zoomPrivacy"),
    path("zoom-tos/", views.zoomTOS, name="zoomTOS"),
    path("zoom-privacy/", views.zoomPrivacy, name="zoomPrivacy"),
    path("zoom-support/", views.zoomSupport, name="zoomTOS"),
    path("zoom-documentation/", views.zoomDocumentation, name="zoomPrivacy"),
    path("sports-betting-money-management/", views.sports_betting_money_management, name="sports_betting_money_management"),
    path("second-opinions/", views.second_opinions, name="second_opinions"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path("predictions/", views.predictions, name="predictions"),
    path("recaps/", views.recaps, name="recaps"),
    path("parlays/", views.parlays, name="parlays"),
    path("topnews/", views.topnews, name="topnews"),
    path("props/", views.props, name="props"),
    path('ajax_handler/<str:sport>',views.ajax_handler,name="ajax_handler"),
    path('ajax_handlerb/<str:sport>',views.ajax_handlerb,name="ajax_handlerb"),
    # new path below...
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"Predictions": GenericSitemap(info_dict),"Parlays": GenericSitemap(info_dict2),"Props": GenericSitemap(info_dict3),"Recaps": GenericSitemap(info_dict4)}},
    ),
    path("stripe/", include("djstripe.urls", namespace="djstripe")), #add this
    path("pricing-page/", views.pricing_page, name="pricing_page"),
]