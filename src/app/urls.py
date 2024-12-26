from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/home/", views.HomeAPIView.as_view(), name="home-api"),
]
