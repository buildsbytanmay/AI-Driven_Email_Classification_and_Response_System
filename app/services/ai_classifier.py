from transformers import pipeline

# Load model once (global)
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

CATEGORIES = ["Spam", "Work", "Personal", "Important"]


def classify_email(text: str):
    result = classifier(text, CATEGORIES)

    label = result["labels"][0]
    score = result["scores"][0]

    return {
        "category": label,
        "confidence": float(score)
    }