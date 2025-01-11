import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Restaurant, Cuisine, Ambience
from tqdm import tqdm


class Command(BaseCommand):
    help = "Load restaurant data from a CSV file into the Restaurant model"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="The path to the CSV file containing restaurant data.",
        )

    def handle(self, *args, **options):
        file_path = options["csv_file"]

        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                restaurants_to_create = []

                for row in tqdm(reader):
                    # ignore closed restaurants (permanently)
                    if row.get("is_open") != "1":
                        continue

                    # Helper function to parse boolean fields
                    def parse_boolean(value):
                        return value == "1"

                    # Parse cuisines and ambiences (comma-separated values)
                    cuisine_cols = [
                        "Bakeries",
                        "Gelato",
                        "Guamanian",
                        "Buffets",
                        "Juice Bars & Smoothies",
                        "Burmese",
                        "Australian",
                        "Kombucha",
                        "Fish & Chips",
                        "Szechuan",
                        "Venezuelan",
                        "Indonesian",
                        "Thai",
                        "Waffles",
                        "Singaporean",
                        "Coffeeshops",
                        "Sushi Bars",
                        "Persian/Iranian",
                        "Syrian",
                        "Pakistani",
                        "Chinese",
                        "Cupcakes",
                        "Hot Dogs",
                        "Tea Rooms",
                        "Korean",
                        "Patisserie/Cake Shop",
                        "Pasta Shops",
                        "Salvadoran",
                        "Japanese Curry",
                        "Halal",
                        "Greek",
                        "Pan Asian",
                        "Beer Hall",
                        "Poutineries",
                        "Pizza",
                        "Senegalese",
                        "Vegetarian",
                        "African",
                        "Turkish",
                        "Hot Pot",
                        "Hawaiian",
                        "Irish",
                        "Soul Food",
                        "Puerto Rican",
                        "Macarons",
                        "Israeli",
                        "Diners",
                        "Cajun/Creole",
                        "Tex-Mex",
                        "Creperies",
                        "Wraps",
                        "Austrian",
                        "Beer Bar",
                        "Wine & Spirits",
                        "Moroccan",
                        "Ukrainian",
                        "American (Traditional)",
                        "Belgian",
                        "Malaysian",
                        "Ethnic Food",
                        "Tacos",
                        "Kosher",
                        "Bangladeshi",
                        "Himalayan/Nepalese",
                        "Mongolian",
                        "Canadian (New)",
                        "Izakaya",
                        "French",
                        "Cuban",
                        "Filipino",
                        "Caterers",
                        "Brazilian",
                        "Spanish",
                        "Wineries",
                        "Parent Cafes",
                        "Asian Fusion",
                        "Delis",
                        "Hong Kong Style Cafe",
                        "Acai Bowls",
                        "Brewpubs",
                        "Tuscan",
                        "Indian",
                        "Burgers",
                        "Brasseries",
                        "British",
                        "Hungarian",
                        "German",
                        "Cafes",
                        "Chocolatiers & Shops",
                        "Bubble Tea",
                        "Beer Gardens",
                        "Coffee Roasteries",
                        "Peruvian",
                        "Tapas Bars",
                        "Sardinian",
                        "Barbeque",
                        "Poke",
                        "Scandinavian",
                        "Egyptian",
                        "South African",
                        "Portuguese",
                        "Food Trucks",
                        "Pita",
                        "Donburi",
                        "Bagels",
                        "Russian",
                        "Southern",
                        "Mediterranean",
                        "Organic Stores",
                        "Health Markets",
                        "Shanghainese",
                        "Local Flavor",
                        "Conveyor Belt Sushi",
                        "Fuzhou",
                        "Noodles",
                        "Latin American",
                        "Scottish",
                        "Irish Pub",
                        "Taiwanese",
                        "Empanadas",
                        "Gluten-Free",
                        "Middle Eastern",
                        "Pancakes",
                        "Cocktail Bars",
                        "Breakfast & Brunch",
                        "Nicaraguan",
                        "Italian",
                        "Tonkatsu",
                        "Themed Cafes",
                        "Ethical Grocery",
                        "Food Stands",
                        "Laotian",
                        "Serbo Croatian",
                        "Desserts",
                        "Iberian",
                        "Lebanese",
                        "Food",
                        "Sicilian",
                        "Fruits & Veggies",
                        "Live/Raw Food",
                        "Hakka",
                        "Bistros",
                        "Food Court",
                        "Custom Cakes",
                        "Falafel",
                        "Dim Sum",
                        "Czech",
                        "Cafeteria",
                        "Dominican",
                        "Cheesesteaks",
                        "Caribbean",
                        "Modern European",
                        "Cambodian",
                        "Kebab",
                        "Arabic",
                        "American (New)",
                        "Pop-Up Restaurants",
                        "Ethnic Grocery",
                        "Oriental",
                        "Georgian",
                        "Coffee & Tea",
                        "Soup",
                        "Argentine",
                        "Colombian",
                        "Comfort Food",
                        "International",
                        "New Mexican Cuisine",
                        "Ramen",
                        "Uzbek",
                        "Dumplings",
                        "Salad",
                        "Do-It-Yourself Food",
                        "Honduran",
                        "Cucina campana",
                        "Fondue",
                        "Seafood",
                        "Basque",
                        "Mexican",
                        "Haitian",
                        "Beer",
                        "Sandwiches",
                        "Pretzels",
                        "Hainan",
                        "Eastern European",
                        "Polish",
                        "Ethiopian",
                        "Wine Bars",
                        "Cideries",
                        "Japanese",
                        "Trinidadian",
                        "Steakhouses",
                        "Vietnamese",
                        "Ice Cream & Frozen Yogurt",
                        "Sri Lankan",
                        "Specialty Food",
                        "Cantonese",
                        "Breweries",
                        "Vegan",
                        "Calabrian",
                        "Donuts",
                        "Chicken Wings",
                    ]
                    ambience_cols = [
                        "divey",
                        "upscale",
                        "touristy",
                        "intimate",
                        "casual",
                        "trendy",
                        "classy",
                        "hipster",
                        "romantic",
                    ]

                    cuisines = [
                        name.strip()
                        for name in row.keys()
                        if name.strip() in cuisine_cols and row.get(name) == "1"
                    ]

                    ambiences = [
                        name.strip()
                        for name in row.keys()
                        if name.strip() in ambience_cols and row.get(name) == "1"
                    ]

                    # Define sustainable categories
                    sustainable_cuisines = [
                        "Vegan",
                        "Vegetarian",
                        "Organic Stores",
                        "Ethical Grocery",
                        "Local Flavor",
                        "Ethnic Grocery",
                    ]

                    # Parse time fields
                    def parse_time(time_str):
                        if time_str:
                            try:
                                return datetime.strptime(time_str, "%H:%M:%S").time()
                            except ValueError:
                                return None
                        return None

                    restaurant = Restaurant(
                        business_id=row["business_id"],
                        name=row["name"],
                        address=row["address"],
                        city=row["city"],
                        state=row["state"],
                        postal_code=row.get("postal_code"),
                        latitude=(
                            float(row["latitude"]) if row.get("latitude") else None
                        ),
                        longitude=(
                            float(row["longitude"]) if row.get("longitude") else None
                        ),
                        review_count=int(row["review_count"]),
                        rating=float(row["stars"]),
                        good_for_kids=parse_boolean(row.get("attributes.GoodForKids")),
                        good_for_groups=parse_boolean(
                            row.get("attributes.RestaurantsGoodForGroups")
                        ),
                        take_out=parse_boolean(
                            row.get("attributes.RestaurantsTakeOut")
                        ),
                        reservations=parse_boolean(
                            row.get("attributes.RestaurantsReservations")
                        ),
                        delivery=parse_boolean(
                            row.get("attributes.RestaurantsDelivery")
                        ),
                        outdoor_seating=parse_boolean(
                            row.get("attributes.OutdoorSeating")
                        ),
                        wheelchair_accessible=parse_boolean(
                            row.get("attributes.WheelchairAccessible")
                        ),
                        bike_parking=parse_boolean(row.get("attributes.BikeParking")),
                        credit_cards_accepted=parse_boolean(
                            row.get("attributes.BusinessAcceptsCreditCards")
                        ),
                        price_range=(
                            int(row["attributes.RestaurantsPriceRange2"])
                            if row.get("attributes.RestaurantsPriceRange2")
                            else None
                        ),
                        alcohol=parse_boolean(row.get("attributes.Alcohol")),
                        happy_hour=parse_boolean(row.get("attributes.HappyHour")),
                        dogs_allowed=parse_boolean(row.get("attributes.DogsAllowed")),
                        sustainable=any(
                            cuisine in sustainable_cuisines for cuisine in cuisines
                        ),
                        parking=parse_boolean(row.get("attributes.BusinessParking")),
                        monday_open=parse_time(row.get("hours.Monday_open_time")),
                        monday_close=parse_time(row.get("hours.Monday_close_time")),
                        tuesday_open=parse_time(row.get("hours.Tuesday_open_time")),
                        tuesday_close=parse_time(row.get("hours.Tuesday_close_time")),
                        wednesday_open=parse_time(row.get("hours.Wednesday_open_time")),
                        wednesday_close=parse_time(
                            row.get("hours.Wednesday_close_time")
                        ),
                        thursday_open=parse_time(row.get("hours.Thursday_open_time")),
                        thursday_close=parse_time(row.get("hours.Thursday_close_time")),
                        friday_open=parse_time(row.get("hours.Friday_open_time")),
                        friday_close=parse_time(row.get("hours.Friday_close_time")),
                        saturday_open=parse_time(row.get("hours.Saturday_open_time")),
                        saturday_close=parse_time(row.get("hours.Saturday_close_time")),
                        sunday_open=parse_time(row.get("hours.Sunday_open_time")),
                        sunday_close=parse_time(row.get("hours.Sunday_close_time")),
                    )
                    restaurant.save()

                    # Add many-to-many relationships
                    for cuisine_name in cuisines:
                        cuisine_obj, _ = Cuisine.objects.get_or_create(
                            name=cuisine_name
                        )
                        restaurant.cuisines.add(cuisine_obj)

                    # Add or fetch ambience instances
                    for ambience_name in ambiences:
                        ambience_obj, _ = Ambience.objects.get_or_create(
                            name=ambience_name
                        )
                        restaurant.ambiences.add(ambience_obj)

                    restaurants_to_create.append(restaurant)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully loaded {len(restaurants_to_create)} restaurants."
                    )
                )

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
        except KeyError as e:
            self.stderr.write(
                self.style.ERROR(f"Missing required column in CSV file: {str(e)}")
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))
