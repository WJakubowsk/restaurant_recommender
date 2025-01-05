import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import User
from tqdm import tqdm


class Command(BaseCommand):
    help = "Load user data from a CSV file into the User model"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="The path to the CSV file containing user data.",
        )

    def handle(self, *args, **options):
        file_path = options["csv_file"]
        csv.field_size_limit(10000000)

        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                users_to_create = []

                for row in tqdm(reader):
                    try:
                        account_since_date = datetime.strptime(
                            row["yelping_since"], "%Y-%m-%d %H:%M:%S"
                        ).date()
                    except ValueError:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Skipping user with invalid date format: {row['user_id']}"
                            )
                        )
                        continue

                    user = User(
                        user_id=row["user_id"],
                        name=row["name"],
                        review_count=int(row["review_count"]),
                        account_since=account_since_date,
                        average_rating=float(row["average_stars"]),
                    )
                    users_to_create.append(user)

                User.objects.bulk_create(users_to_create)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully loaded {len(users_to_create)} users."
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
