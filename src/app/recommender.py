import numpy as np
import pandas as pd


class Recommender:
    def __init__(self, businesses, reviews):
        self.businesses = businesses
        self.reviews = reviews
        self.user_weights = None
        self.target_user_id = None

    def prepare_features(self, df):
        # Remove unnecessary columns
        feature_df = df.drop(
            [
                "postal_code",
                "city",
                "state",
                "address",
                "name",
                "latitude",
                "longitude",
                "monday_open",
                "monday_close",
                "tuesday_open",
                "tuesday_close",
                "wednesday_open",
                "wednesday_close",
                "thursday_open",
                "thursday_close",
                "friday_open",
                "friday_close",
                "saturday_open",
                "saturday_close",
                "sunday_open",
                "sunday_close",
            ],
            axis=1,
        )
        # print(feature_df.head())
        # Take business_id as index
        feature_df.set_index("business_id", inplace=True)
        # Normalize stars and review_count
        feature_df["rating"] = (
            feature_df["rating"] - feature_df["rating"].mean()
        ) / feature_df["rating"].std()
        feature_df["review_count"] = (
            feature_df["review_count"] - feature_df["review_count"].mean()
        ) / feature_df["review_count"].std()
        return feature_df

    def fit(self, user_id):
        reviews_df = pd.DataFrame.from_records(self.reviews.values())
        self.target_user_id = user_id
        user_reviews = reviews_df[reviews_df["user_id_id"] == user_id]

        if user_reviews.empty:
            self.user_weights = None
        else:
            user_businesses = self.businesses[
                self.businesses["business_id_id"].isin(user_reviews["business_id_id"])
            ]
            features = self.prepare_features(user_businesses)
            ratings = user_reviews["rating"]
            self.user_weights = np.dot(ratings.values, features.values)

    def predict(self, businesses, top_n=500):
        # Convert the queryset to a DataFrame for processing
        businesses_df = pd.DataFrame.from_records(businesses.values())

        # Prepare features for the filtered businesses
        all_features = self.prepare_features(businesses_df)

        if self.user_weights is None:
            # Recommend top-rated restaurants (bestsellers) if no reviews
            return businesses.order_by("-rating")[:top_n]

        # Compute recommendation scores using vectorized dot product
        scores = np.dot(all_features.values, self.user_weights) / np.sum(
            self.user_weights
        )

        # Add scores to the DataFrame
        businesses_df["recommendation_score"] = scores

        # Sort by recommendation score and get top N
        top_recommendations = businesses_df.sort_values(
            by="recommendation_score", ascending=False
        ).head(top_n)

        # Filter the original queryset to include only the top recommendations
        return businesses.filter(
            business_id__in=top_recommendations["business_id_id"]
        ).order_by("-recommendation_score")
