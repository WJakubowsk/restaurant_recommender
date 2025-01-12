from datetime import date, datetime

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Restaurant, Review
from .forms import RestaurantFilterForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as AuthUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.apps import apps

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RestaurantFilterForm
from .models import Restaurant, Cuisine, Review, Ambience, User as CustomUser

import json
import torch


from .recommender import Recommender

@api_view(["POST"])
def signup(request):
    """
    Signup a new user
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if AuthUser.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    if AuthUser.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Create the Django authentication user
    auth_user = AuthUser.objects.create_user(
        username=username, email=email, password=password
    )

    # Create the corresponding custom User model entry
    custom_user = CustomUser.objects.create(
        user_id=auth_user.id,  # Link to the AuthUser id
        name=username,
        account_since=date.today(),
        average_rating=0.0,
    )

    # Generate a token for the newly created user
    token, _ = Token.objects.get_or_create(user=auth_user)

    return Response(
        {
            "token": token.key,
            "username": auth_user.username,
            "user_id": custom_user.user_id,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def login_view(request):
    """
    Login a user
    """
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "username": user.username}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class HomeAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Restaurant Recommender!"})


def cuisine_list(request):
    cuisines = Cuisine.objects.all().values("id", "name")  # Return id and name
    return JsonResponse(list(cuisines), safe=False)


def ambience_list(request):
    ambiences = Ambience.objects.all().values("id", "name")  # Return id and name
    return JsonResponse(list(ambiences), safe=False)


def home(request):
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
            if name != "" and name is not None:
                restaurants = restaurants.filter(name__icontains=name)

            if cuisine != "" and cuisine is not None:
                # `cuisine` is a Cuisine instance because of ModelChoiceField
                restaurants = restaurants.filter(cuisines__id=cuisine.id)

            if ambience != "" and ambience is not None:
                # Ambience is received as an ID, filter by it
                restaurants = restaurants.filter(ambiences__id=ambience.id)

            if min_rating != "" and min_rating is not None:
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
            if city != "" and city is not None:
                restaurants = restaurants.filter(city__icontains=city)
            if price_range != "" and price_range is not None:
                restaurants = restaurants.filter(price_range=int(price_range))
            if delivery != "" and delivery is not None and delivery is not False:
                restaurants = restaurants.filter(delivery=delivery)
            if (
                good_for_kids != ""
                and good_for_kids is not None
                and good_for_kids is not False
            ):
                restaurants = restaurants.filter(good_for_kids=good_for_kids)
            if (
                good_for_groups != ""
                and good_for_groups is not None
                and good_for_groups is not False
            ):
                restaurants = restaurants.filter(good_for_groups=good_for_groups)

            if take_out != "" and take_out is not None and take_out is not False:
                restaurants = restaurants.filter(take_out=take_out)
            if (
                reservations != ""
                and reservations is not None
                and reservations is not False
            ):
                restaurants = restaurants.filter(reservations=reservations)
            if (
                outdoor_seating != ""
                and outdoor_seating is not None
                and outdoor_seating is not False
            ):
                restaurants = restaurants.filter(outdoor_seating=outdoor_seating)
            if (
                wheelchair_accessible != ""
                and wheelchair_accessible is not None
                and wheelchair_accessible is not False
            ):
                restaurants = restaurants.filter(
                    wheelchair_accessible=wheelchair_accessible
                )
            if (
                bike_parking != ""
                and bike_parking is not None
                and bike_parking is not False
            ):
                restaurants = restaurants.filter(bike_parking=bike_parking)
            if (
                credit_cards_accepted != ""
                and credit_cards_accepted is not None
                and credit_cards_accepted is not False
            ):
                restaurants = restaurants.filter(
                    credit_cards_accepted=credit_cards_accepted
                )

            if happy_hour != "" and happy_hour is not None and happy_hour is not False:
                restaurants = restaurants.filter(happy_hour=happy_hour)
            if (
                dogs_allowed != ""
                and dogs_allowed is not None
                and dogs_allowed is not False
            ):
                restaurants = restaurants.filter(dogs_allowed=dogs_allowed)
            if (
                sustainable != ""
                and sustainable is not None
                and sustainable is not False
            ):
                restaurants = restaurants.filter(sustainable=sustainable)
            now = datetime.now()
            current_day = now.strftime("%A").lower()  # e.g., "monday", "tuesday"
            current_time = now.time()

            # Dynamically filter based on opening and closing times
            open_field = f"{current_day}_open"
            close_field = f"{current_day}_close"

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                print("Calling recommender function")    
                recommender = Recommender(businesses=restaurants, reviews=Review.objects.all())
                recommender.fit(user_id=request.user.id)  # Fit with the current user's data
                top_recommendations = recommender.predict(businesses=restaurants)
                print("Top recommendations",top_recommendations)

                if top_recommendations.count()>500:    
                    limited_restaurants = top_recommendations[:500]
                    restaurant_data = [
                        {
                            "name": restaurant.name,
                            "cuisine": [
                                c.name for c in restaurant.cuisines.all()
                            ],  # Extract related field
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
                        for restaurant in limited_restaurants
                    ]

                    return JsonResponse({"restaurants": restaurant_data}, safe=False)
                else:

                    restaurant_data = [
                        {
                            "name": restaurant.name,
                            "cuisine": [
                                c.name for c in restaurant.cuisines.all()
                            ],  # Extract related field
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
                        for restaurant in top_recommendations
                    ]
                    
                    # return render(
                    #         request, "restaurant_list.html", {"form": form, "restaurants": top_recommendations}
                    #     )
                    return JsonResponse({"restaurants": restaurant_data}, safe=False)


    else:
        form = RestaurantFilterForm()

    return render(
        request, "restaurant_list.html", {"form": form, "restaurants": restaurants}
    )


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        restaurant_name = data.get("restaurant_name", "").strip()
        rating = data.get("rating")
        text = data.get("text")

        print(f"Received restaurant_name: {restaurant_name}")  # Debugging
        print(f"Received rating: {rating}, text: {text}")  # Debugging

        restaurant = Restaurant.objects.filter(name__iexact=restaurant_name).first()
        if not restaurant:
            return JsonResponse(
                {"error": f"Restaurant '{restaurant_name}' does not exist."}, status=400
            )

        # Check if the review is AI-generated
        is_ai_generated = filter_review(text)
        if is_ai_generated:
            return JsonResponse(
                {
                    "message": "Your review appears to be AI-generated. Please revise it and try again."
                },
                status=400,
            )

        # Create the review if not AI-generated
        review = Review.objects.create(
            review_id=Review.objects.count() + 1,
            user_id=CustomUser.objects.first(),  # Replace with authenticated user logic
            business_id=restaurant,
            rating=rating,
            text=text,
            date=date.today(),
        )

        # Update user statistics if authenticated
        if request.user.is_authenticated:
            request.user.review_count += 1
            request.user.average_rating = (
                (request.user.average_rating * (request.user.review_count - 1)) + rating
            ) / request.user.review_count
            request.user.save()

        return JsonResponse(
            {
                "message": "Thank you for your review! It has been submitted successfully."
            },
            status=201,
        )

    return JsonResponse({"error": "Invalid request method."}, status=405)


def autocomplete_restaurants(request):
    if "term" in request.GET:
        qs = Restaurant.objects.filter(name__icontains=request.GET.get("term"))[:10]
        names = list(qs.values_list("name", flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


def filter_review(review_text: str) -> str:
    # Access the pre-loaded model and tokenizer from the AppConfig
    filter_config = apps.get_app_config("app")
    model = filter_config.model
    tokenizer = filter_config.tokenizer
    device = filter_config.device

    inputs = tokenizer(review_text, return_tensors="pt", padding=True, truncation=True)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        prediction = torch.argmax(probs, dim=-1).item()

    return True if prediction == 1 else False
