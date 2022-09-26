from turtle import home
from tweet_handler import views
from django.urls import path
from tweet_handler.views import home

urlpatterns = [
    path('5436384513:AAGN5E9edKOmvvZdHE1QIcTGhIR60Mx1n84', home),
    path('set_webhook/', views.set_webhook),
    path('tweet_stream/', views.tweet_stream)

]