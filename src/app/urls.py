from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("api/home/", views.HomeAPIView.as_view(), name="home-api"),
    path("api/restaurants/", views.home, name="restaurants-api"),
    path("api/cuisines/", views.cuisine_list, name="cuisine_list"),
    path("api/ambiences/", views.ambience_list, name="ambience_list"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("add_review/", views.add_review, name="add_review"),
]
