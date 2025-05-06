from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def load_sentiment_pipeline():
    model_name = "w11wo/indonesian-roberta-base-sentiment-classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

sentiment_pipeline = load_sentiment_pipeline()

def analyze_sentiment(comment):
    return sentiment_pipeline(comment)[0]["label"]
