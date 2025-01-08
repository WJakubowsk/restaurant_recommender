from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Restaurant
from .forms import RestaurantFilterForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
@api_view(['POST'])
def signup(request):
    """
    Signup a new user
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    """
    Login a user
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class HomeAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Restaurant Recommender!"})

from django.http import JsonResponse
from .models import Cuisine

def cuisine_list(request):
    cuisines = Cuisine.objects.all().values("id", "name")  # Return id and name
    return JsonResponse(list(cuisines), safe=False)

from .models import Ambience

def ambience_list(request):
    ambiences = Ambience.objects.all().values("id", "name")  # Return id and name
    return JsonResponse(list(ambiences), safe=False)


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
            ambience = form.cleaned_data.get("ambience")
            min_rating = form.cleaned_data.get("min_rating")
            open_now = form.cleaned_data.get("open_now")
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
            sustainable = form.cleaned_data.get("sustainable")

            

            # Apply filters
            if name:
                restaurants = restaurants.filter(name__icontains=name)
         
            if cuisine:
    # `cuisine` is a Cuisine instance because of ModelChoiceField
                 restaurants = restaurants.filter(cuisines__id=cuisine.id)

            if ambience:
                # Ambience is received as an ID, filter by it
                restaurants = restaurants.filter(ambiences__id=ambience.id)


            if min_rating is not None:
                restaurants = restaurants.filter(rating__gte=min_rating)
            if open_now:
                # Determine current day and time
                now = datetime.now()
                current_day = now.strftime("%A").lower()  # e.g., "monday", "tuesday"
                current_time = now.time()

                # Dynamically filter based on opening and closing times
                open_field = f"{current_day}_open"
                close_field = f"{current_day}_close"

                restaurants = restaurants.filter(
                    **{
                        f"{open_field}__lte": current_time,  # Open before or at the current time
                        f"{close_field}__gte": current_time,  # Close after or at the current time
                    }
                )
            if city:
                restaurants = restaurants.filter(city__icontains=city)
            if price_range:
                 restaurants = restaurants.filter(price_range=int(price_range))

            if delivery is not None:
                restaurants = restaurants.filter(delivery=delivery)
            if good_for_kids is not None:
                restaurants = restaurants.filter(good_for_kids=good_for_kids)
            if good_for_groups is not None :
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
            if sustainable is not None:
                restaurants = restaurants.filter(sustainable=sustainable)
            now = datetime.now()
            current_day = now.strftime("%A").lower()  # e.g., "monday", "tuesday"
            current_time = now.time()

                # Dynamically filter based on opening and closing times
            open_field = f"{current_day}_open"
            close_field = f"{current_day}_close"
            

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                restaurant_data = [
                    {
                        "name": restaurant.name,
                        "cuisine": [c.name for c in restaurant.cuisines.all()],  # Extract related field
                        "ambience": [a.name for a in restaurant.ambiences.all()],
                        "rating": restaurant.rating,
                        "city": restaurant.city,
                        "price_range": restaurant.price_range,
                        "delivery": restaurant.delivery,
                        "good_for_kids": restaurant.good_for_kids,
                        "good_for_groups": restaurant.good_for_groups,
                        "take_out": restaurant.take_out,
                        "reservations": restaurant.reservations,
                        "outdoor_seating": restaurant.outdoor_seating,
                        "wheelchair_accessible": restaurant.wheelchair_accessible,
                        "bike_parking": restaurant.bike_parking,
                        "credit_cards_accepted": restaurant.credit_cards_accepted,
                        "happy_hour": restaurant.happy_hour,
                        "dogs_allowed": restaurant.dogs_allowed,
                        "sustainable": restaurant.sustainable,
                        "latitude": restaurant.latitude,
                        "longitude": restaurant.longitude,
                         "monday_open": restaurant.monday_open,
                        "monday_close": restaurant.monday_close,
                        "tuesday_open": restaurant.tuesday_open,
                        "tuesday_close": restaurant.tuesday_close,
                        "wednesday_open": restaurant.wednesday_open,
                        "wednesday_close": restaurant.wednesday_close,
                        "thursday_open": restaurant.thursday_open,
                        "thursday_close": restaurant.thursday_close,
                        "friday_open": restaurant.friday_open,
                        "friday_close": restaurant.friday_close,
                        "saturday_open": restaurant.saturday_open,
                        "saturday_close": restaurant.saturday_close,
                        "sunday_open": restaurant.sunday_open,
                        "sunday_close": restaurant.sunday_close,
                    }
                    for restaurant in restaurants
                ]
                return JsonResponse({"restaurants": restaurant_data}, safe=False)
    else:
        form = RestaurantFilterForm()

    print(form.errors)
    # Render the template with the filtered restaurants and the form
    return render(
        request, "restaurant_list.html", {"form": form, "restaurants": restaurants}
    )

