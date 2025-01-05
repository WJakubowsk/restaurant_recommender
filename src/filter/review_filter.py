from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
)
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm


# Define a custom dataset
class ReviewDataset(Dataset):
    def __init__(self, reviews, tokenizer):
        self.reviews = reviews
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.reviews)

    def __getitem__(self, idx):
        # Tokenize and return only necessary fields
        return self.tokenizer(self.reviews[idx], truncation=True, padding=False)


def get_sample_reviews(df: pd.DataFrame, n: int = 1000000):
    """
    Get a sample of reviews from the dataframe - 1 million by default
    """
    df = df[["review_id", "user_id", "business_id", "stars", "date", "text"]]
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date", ascending=False)
    df = df.head(n)
    df.to_csv("../../data/yelp_academic_dataset_review_1MLN.csv", index=False)


def filter_reviews(df: pd.DataFrame) -> pd.DataFrame:
    # Load the model and tokenizer
    model_name = "zayuki/computer_generated_fake_review_detection"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, from_tf=True)

    # Check for GPU availability and move the model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Create dataset and dataloader
    dataset = ReviewDataset(df["text"].tolist(), tokenizer)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    dataloader = DataLoader(dataset, batch_size=16, collate_fn=data_collator)

    # Process batches
    classifications = []
    for batch in tqdm(dataloader):
        # Prepare inputs for the model
        inputs = {key: value.to(device) for key, value in batch.items()}
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predictions = torch.argmax(probs, dim=-1).tolist()
        classifications.extend(
            ["fake" if pred == 1 else "genuine" for pred in predictions]
        )

    # Update the dataframe with classifications
    df["classification"] = classifications
    return df


if __name__ == "__main__":
    # Load data
    df = pd.read_csv("../../data/yelp_academic_dataset_review_1MLN.csv")
    # Filter reviews
    df = filter_reviews(df)
    # Save the filtered reviews
    df.to_csv("../../data/yelp_academic_dataset_review_1MLN_filtered.csv", index=False)
