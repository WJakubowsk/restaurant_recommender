from django.apps import AppConfig
import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class ReviewFilterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    verbose_name = "Review Filter"

    def ready(self):
        # Suppress logging for transformers, TF and torch
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = (
            "2"  # Suppresses INFO and WARNING from TensorFlow
        )
        logging.getLogger("transformers").setLevel(logging.ERROR)
        logging.getLogger("torch").setLevel(logging.ERROR)
        logging.getLogger("tensorflow").setLevel(logging.ERROR)
        # Load the model and tokenizer when the app is ready
        self.model_name = "zayuki/computer_generated_fake_review_detection"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name, from_tf=True
        )

        # Check for GPU availability and move the model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        print("Model loaded and ready.")
