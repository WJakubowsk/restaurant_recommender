from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response


class HomeAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Restaurant Recommender!"})


def home(request):
    return HttpResponse("Welcome to the Fresh Restaurant Recommender!")
