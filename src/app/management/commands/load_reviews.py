import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import Review, User, Restaurant
from tqdm import tqdm


class Command(BaseCommand):
    help = "Load reviews from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="The path to the CSV file.")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        try:
            with open(csv_file, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in tqdm(reader):
                    if row["classification"].lower() == "genuine":
                        try:
                            # Retrieve the Restaurant and User instances
                            try:
                                restaurant = Restaurant.objects.get(
                                    business_id=row["business_id"]
                                )
                                user = User.objects.get(user_id=row["user_id"])
                            except Restaurant.DoesNotExist:
                                self.stderr.write(
                                    f"Restaurant with business_id {row['business_id']} not found."
                                )
                                continue  # Skip this review if the restaurant doesn't exist
                            except User.DoesNotExist:
                                self.stderr.write(
                                    f"User with user_id {row['user_id']} not found."
                                )
                                continue  # Skip this review if the user doesn't exist

                            # Create and save the review
                            review = Review(
                                review_id=row["review_id"],
                                user_id=user,  # Assign the User instance
                                business_id=restaurant,
                                rating=float(row["stars"]),
                                date=datetime.strptime(
                                    row["date"], "%Y-%m-%d %H:%M:%S"
                                ),
                                text=row["text"],
                            )
                            review.save()
                            # self.stdout.write(f"Saved review {row['review_id']}")

                        except User.DoesNotExist:
                            self.stderr.write(
                                f"User with ID {row['user_id']} not found."
                            )
        except FileNotFoundError:
            self.stderr.write(f"File {csv_file} not found.")
        except Exception as e:
            self.stderr.write(str(e))
