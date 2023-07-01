
from django.contrib import admin
from django.urls import path
from main.views import HomePageView, CRUDView, RequestsView



urlpatterns = [
        path('', HomePageView.as_view(), name='home'),
        path('users', CRUDView.as_view(), name='users'),
        path('requests',RequestsView.as_view(), name='requests'),
    ]   


