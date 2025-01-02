from django import forms
from .models import Restaurant, Cuisine


class RestaurantFilterForm(forms.Form):
    # Filter by cuisine
    cuisine = forms.ModelChoiceField(queryset=Cuisine.objects.all(), required=False)

    # Filter by rating (1 to 5 with 0.5 increments)
    min_rating = forms.DecimalField(
        required=False,
        max_digits=2,
        decimal_places=1,
        min_value=1.0,
        max_value=5.0,
        label="Min Rating",
        widget=forms.NumberInput(attrs={"step": "0.5"}),
    )

    # Filter by location (city)
    city = forms.CharField(max_length=100, required=False, label="City")

    # Filter by price range
    price_range = forms.ChoiceField(
        choices=[(1, "$"), (2, "$$"), (3, "$$$"), (4, "$$$$")], required=False
    )

    # Boolean fields for restaurant features
    good_for_kids = forms.BooleanField(required=False, label="Good for Kids")
    good_for_groups = forms.BooleanField(required=False, label="Good for Groups")
    take_out = forms.BooleanField(required=False, label="Take Out")
    reservations = forms.BooleanField(required=False, label="Reservations")
    delivery = forms.BooleanField(required=False, label="Delivery")
    outdoor_seating = forms.BooleanField(required=False, label="Outdoor Seating")
    wheelchair_accessible = forms.BooleanField(
        required=False, label="Wheelchair Accessible"
    )
    bike_parking = forms.BooleanField(required=False, label="Bike Parking")
    credit_cards_accepted = forms.BooleanField(
        required=False, label="Credit Cards Accepted"
    )
    happy_hour = forms.BooleanField(required=False, label="Happy Hour")
    dogs_allowed = forms.BooleanField(required=False, label="Dogs Allowed")
    delivery = forms.BooleanField(
        required=False, label="Offers Delivery", initial=False
    )
