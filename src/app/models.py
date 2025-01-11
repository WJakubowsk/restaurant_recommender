from django.db import models


# Restaurant model
class Restaurant(models.Model):
    # Basic Information
    business_id = models.CharField(max_length=22, unique=True, default="-1")
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100, default="unkown")
    state = models.CharField(max_length=2, default="unkown")
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

    # Attributes
    good_for_kids = models.BooleanField(null=True, blank=True)
    good_for_groups = models.BooleanField(null=True, blank=True)
    take_out = models.BooleanField(null=True, blank=True)
    reservations = models.BooleanField(null=True, blank=True)
    delivery = models.BooleanField(null=True, blank=True)
    outdoor_seating = models.BooleanField(null=True, blank=True)
    wheelchair_accessible = models.BooleanField(null=True, blank=True)
    bike_parking = models.BooleanField(null=True, blank=True)
    credit_cards_accepted = models.BooleanField(null=True, blank=True)
    price_range = models.IntegerField(null=True, blank=True)
    alcohol = models.BooleanField(null=True, blank=True)
    happy_hour = models.BooleanField(null=True, blank=True)
    dogs_allowed = models.BooleanField(null=True, blank=True)
    sustainable = models.BooleanField(null=True, blank=True)

    # Cuisine & ambience categories (Many-to-Many Relationship)
    cuisines = models.ManyToManyField("Cuisine", related_name="restaurants", blank=True)
    ambiences = models.ManyToManyField(
        "Ambience", related_name="restaurants", blank=True
    )

    # Parking Information
    parking = models.BooleanField(null=True, blank=True)

    # Operating Hours
    monday_open = models.TimeField(null=True, blank=True)
    monday_close = models.TimeField(null=True, blank=True)
    tuesday_open = models.TimeField(null=True, blank=True)
    tuesday_close = models.TimeField(null=True, blank=True)
    wednesday_open = models.TimeField(null=True, blank=True)
    wednesday_close = models.TimeField(null=True, blank=True)
    thursday_open = models.TimeField(null=True, blank=True)
    thursday_close = models.TimeField(null=True, blank=True)
    friday_open = models.TimeField(null=True, blank=True)
    friday_close = models.TimeField(null=True, blank=True)
    saturday_open = models.TimeField(null=True, blank=True)
    saturday_close = models.TimeField(null=True, blank=True)
    sunday_open = models.TimeField(null=True, blank=True)
    sunday_close = models.TimeField(null=True, blank=True)

    def __str__(self):
        return (
            "Restaurant: "
            + self.name
            + " in "
            + self.city
            + ", "
            + self.state
            + "average rating: "
            + str(self.rating)
            + " with "
            + str(self.review_count)
            + " reviews"
            + "cuisines: "
            + str(self.cuisines.all())
            + "ambiences: "
            + str(self.ambiences.all())
        )


class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ambience(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# User model
class User(models.Model):
    # Unique identifier
    user_id = models.CharField(
        max_length=22, unique=True, default="-1"
    )  # 22 character unique user ID

    # User details
    name = models.CharField(max_length=100)  # User's first name
    review_count = models.PositiveIntegerField(default=0)  # Number of reviews written
    account_since = models.DateField()  # Date when the user joined
    average_rating = models.FloatField()  # Average rating of all reviews

    def __str__(self):
        return self.name


# Rating model
class Review(models.Model):
    # Unique identifiers
    review_id = models.CharField(max_length=22, unique=True, default="-1")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    business_id = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="reviews"
    )

    # Review details
    rating = models.FloatField()  # Star rating (1.0, 1.5, ..., 4.5, 5.0)
    date = models.DateField()  # Review date
    text = models.TextField()

    def __str__(self):
        return f"Review {self.review_id} from user {self.user_id} for Business {self.business_id}"
