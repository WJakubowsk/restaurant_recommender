import json
import ast
import pandas as pd
import argparse
import warnings
warnings.filterwarnings("ignore")

# Helper function to safely evaluate a string as a dictionary
def safe_eval(val):
    """Safely evaluate a string as a dictionary, return None if invalid."""
    if pd.isna(val):
        return None
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return None

# Load configuration once
def load_config(config_path="config.json"):
    """Load the JSON configuration file."""
    with open(config_path, "r") as file:
        return json.load(file)

# Function to handle categories
def handle_categories(df, config):
    """
    Filter and preprocess the 'categories' column:
    - Keep records with 'Restaurants' or 'Food', excluding 'Groceries'.
    - Remove irrelevant categories.
    - Perform one-hot encoding for relevant categories.
    """
    df = df[
        df['categories'].str.contains('Restaurants|Food', na=False, case=False) &
        ~df['categories'].str.contains('Groceries', na=False, case=False)
    ]

    irrelevant_categories = config["irrelevant_categories"]
    df['categories_list'] = df['categories'].apply(lambda x: [c.strip() for c in x.split(',')])
    df['filtered_categories'] = df['categories_list'].apply(lambda x: [c for c in x if c not in irrelevant_categories])

    # Create one-hot encoded columns
    all_categories = set(cat for categories in df['filtered_categories'] for cat in categories)
    for category in all_categories:
        df[category] = df['filtered_categories'].apply(lambda x: 1 if category in x else 0)

    return df

# Function to preprocess 'Ambience'
def preprocess_ambience(df):
    """Expand the 'attributes.Ambience' column into individual columns."""
    df['attributes.Ambience'] = df['attributes.Ambience'].apply(safe_eval)
    unique_keys = set(
        key for ambience in df['attributes.Ambience']
        if isinstance(ambience, dict) for key in ambience.keys()
    )

    for key in unique_keys:
        df[key] = df['attributes.Ambience'].apply(
            lambda x: 1 if isinstance(x, dict) and x.get(key, False) else 0
        )

    return df

# Function to preprocess parking
def preprocess_parking(df):
    """Create a 'parking' column based on parking availability."""
    df['attributes.BusinessParking'] = df['attributes.BusinessParking'].apply(safe_eval)
    df['attributes.BusinessParking'] = df['attributes.BusinessParking'].apply(
        lambda x: 1 if isinstance(x, dict) and any(x.get(k, False) for k in ['lot', 'garage', 'street']) else 0
    )
    return df

# Function to preprocess alcohol availability
def preprocess_alcohol(df):
    """Convert 'attributes.Alcohol' to a binary column."""
    df['attributes.Alcohol'].fillna('none', inplace=True)
    df['attributes.Alcohol'] = df['attributes.Alcohol'].str.strip("u'")
    df['attributes.Alcohol'] = df['attributes.Alcohol'].apply(lambda x: 0 if x == 'none' else 1)
    return df

# Function to impute price range
def impute_price_range(df):
    """Impute missing or zero values in 'attributes.RestaurantsPriceRange2'."""
    df['attributes.RestaurantsPriceRange2'] = df['attributes.RestaurantsPriceRange2'].fillna(0).astype(int)
    mean_price = df['attributes.RestaurantsPriceRange2'].mean()
    df['attributes.RestaurantsPriceRange2'] = df['attributes.RestaurantsPriceRange2'].replace(0, int(mean_price))
    return df

# Function to impute binary columns
def impute_binary_cols(df, config):
    """Impute binary columns with 0 or 1."""
    binary_cols = config["binary_cols_to_impute"]
    for col in binary_cols:
        df[col] = df[col].apply(lambda x: 1 if x is True else 0)
    return df

# Function to preprocess hours
def preprocess_hours(df, config):
    """Split and preprocess hour columns into open and close times."""
    hours_cols = config["hours_cols"]
    for col in hours_cols:
        df[[f"{col}_open_time", f"{col}_close_time"]] = df[col].str.split('-', expand=True)
        df[f"{col}_open_time"] = pd.to_datetime(df[f"{col}_open_time"], format='%H:%M', errors='coerce').dt.time
        df[f"{col}_close_time"] = pd.to_datetime(df[f"{col}_close_time"], format='%H:%M', errors='coerce').dt.time
    return df

# Main preprocessing function
def preprocess_business(df, config_path="config.json"):
    """Preprocess the business dataset."""
    config = load_config(config_path)

    df = handle_categories(df, config)
    df = preprocess_ambience(df)
    df = preprocess_parking(df)
    df = preprocess_alcohol(df)
    df = impute_price_range(df)
    df = impute_binary_cols(df, config)
    df = preprocess_hours(df, config)


    # Drop columns with more than 80% missing values
    df = df.dropna(axis=1, thresh=0.2*df.shape[0])

    # Drop unwanted columns
    cols_to_drop = config["cols_to_drop"]
    df.drop(cols_to_drop, axis=1, inplace=True)

    return df

# Main function
def main():
    """Main function to preprocess the dataset."""
    # Load the dataset
    parser = argparse.ArgumentParser(
        description='Preprocess business data.'
    )
    parser.add_argument(
        'csv_file',
        type=str,
        help='The business csv file.',
    )
    args = parser.parse_args()

    input_file = args.csv_file
    output_file = f"{input_file.rsplit('.csv', 1)[0]}_preprocessed.csv"
    df = pd.read_csv(input_file)

    # Preprocess the data
    processed_df = preprocess_business(df)

    # Save the processed data
    processed_df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

# Entry point
if __name__ == "__main__":
    main()
