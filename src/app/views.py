from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Restaurant
from .forms import RestaurantFilterForm
from django.contrib.auth.decorators import login_required


class HomeAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Restaurant Recommender!"})


# @login_required
def home(request):
    # Default queryset (all restaurants)
    restaurants = Restaurant.objects.all()

    # Handle form submission
    if request.method == "GET":
        form = RestaurantFilterForm(request.GET)

        if form.is_valid():
            # Get the filter values from the form
            name = form.cleaned_data.get("name")
            cuisine = form.cleaned_data.get("cuisine")
            min_rating = form.cleaned_data.get("min_rating")
            city = form.cleaned_data.get("city")
            price_range = form.cleaned_data.get("price_range")
            delivery = form.cleaned_data.get("delivery")
            good_for_kids = form.cleaned_data.get("good_for_kids")
            good_for_groups = form.cleaned_data.get("good_for_groups")
            take_out = form.cleaned_data.get("take_out")
            reservations = form.cleaned_data.get("reservations")
            outdoor_seating = form.cleaned_data.get("outdoor_seating")
            wheelchair_accessible = form.cleaned_data.get("wheelchair_accessible")
            bike_parking = form.cleaned_data.get("bike_parking")
            credit_cards_accepted = form.cleaned_data.get("credit_cards_accepted")
            happy_hour = form.cleaned_data.get("happy_hour")
            dogs_allowed = form.cleaned_data.get("dogs_allowed")

            # Apply filters
            if name:
                restaurants = restaurants.filter(name__icontains=name)
            if cuisine:
                restaurants = restaurants.filter(cuisine__icontains=cuisine)
            if min_rating is not None:
                restaurants = restaurants.filter(rating__gte=min_rating)
            if city:
                restaurants = restaurants.filter(city__icontains=city)
            if price_range:
                restaurants = restaurants.filter(price_range=price_range)
            if delivery is not None:
                restaurants = restaurants.filter(delivery=delivery)
            if good_for_kids is not None:
                restaurants = restaurants.filter(good_for_kids=good_for_kids)
            if good_for_groups is not None:
                restaurants = restaurants.filter(good_for_groups=good_for_groups)
            if take_out is not None:
                restaurants = restaurants.filter(take_out=take_out)
            if reservations is not None:
                restaurants = restaurants.filter(reservations=reservations)
            if outdoor_seating is not None:
                restaurants = restaurants.filter(outdoor_seating=outdoor_seating)
            if wheelchair_accessible is not None:
                restaurants = restaurants.filter(
                    wheelchair_accessible=wheelchair_accessible
                )
            if bike_parking is not None:
                restaurants = restaurants.filter(bike_parking=bike_parking)
            if credit_cards_accepted is not None:
                restaurants = restaurants.filter(
                    credit_cards_accepted=credit_cards_accepted
                )
            if happy_hour is not None:
                restaurants = restaurants.filter(happy_hour=happy_hour)
            if dogs_allowed is not None:
                restaurants = restaurants.filter(dogs_allowed=dogs_allowed)
    else:
        form = RestaurantFilterForm()

    # Render the template with the filtered restaurants and the form
    return render(
        request, "restaurant_list.html", {"form": form, "restaurants": restaurants}
    )
