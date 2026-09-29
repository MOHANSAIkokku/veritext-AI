from transformers import pipeline

# Hugging Face model
MODEL_NAME = "roberta-base-openai-detector"

print("=" * 60)
print("Loading Hugging Face model...")
print(f"Model: {MODEL_NAME}")
print("=" * 60)

classifier = pipeline(
    "text-classification",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME
)

print("Hugging Face model loaded successfully!")


def classify_text(text: str):
    """
    Classify a piece of text using the Hugging Face model.
    """

    text = text.strip()

    if not text:
        return {
            "label": "UNKNOWN",
            "confidence": 0.0
        }

    # Keep input manageable for the initial MVP.
    text = text[:2000]

    result = classifier(text)

    prediction = result[0]

    return {
        "label": prediction["label"],
        "confidence": round(prediction["score"] * 100, 2)
    }