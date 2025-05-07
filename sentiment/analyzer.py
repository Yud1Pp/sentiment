import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def load_sentiment_pipeline():
    model_name = "w11wo/indonesian-roberta-base-sentiment-classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Cek apakah CUDA tersedia
    device = 0 if torch.cuda.is_available() else -1

    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

sentiment_pipeline = load_sentiment_pipeline()

def analyze_sentiment(comment):
    # Cek apakah komentar kosong setelah preprocessing
    if not comment.strip():
        return "unknown"  # atau "unknown"
    elif comment == "komentar temu":
        return "unknown"
    return sentiment_pipeline(comment)[0]["label"]