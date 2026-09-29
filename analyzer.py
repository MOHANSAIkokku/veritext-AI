import re

from model import classify_text


def clean_text(text: str) -> str:
    """
    Basic text cleaning.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_into_chunks(
    text: str,
    words_per_chunk: int = 120
):
    """
    Split text into manageable chunks.
    """

    words = text.split()

    chunks = []

    for start in range(
        0,
        len(words),
        words_per_chunk
    ):

        chunk = " ".join(
            words[start:start + words_per_chunk]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def analyze_document(text: str):
    """
    Analyze the complete document.
    """

    cleaned_text = clean_text(text)

    if not cleaned_text:
        raise ValueError(
            "No readable text was found."
        )

    chunks = split_into_chunks(cleaned_text)

    results = []

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        prediction = classify_text(chunk)

        results.append({
            "chunk": index,
            "text": chunk,
            "label": prediction["label"],
            "confidence": prediction["confidence"]
        })

    if not results:
        raise ValueError(
            "The document does not contain enough text."
        )

    # Calculate average confidence
    average_confidence = sum(
        item["confidence"]
        for item in results
    ) / len(results)

    # Count labels
    label_counts = {}

    for item in results:

        label = item["label"]

        label_counts[label] = (
            label_counts.get(label, 0) + 1
        )

    # Most common prediction
    overall_label = max(
        label_counts,
        key=label_counts.get
    )

    # Convert label to readable text
    readable_label = convert_label(overall_label)

    return {
        "overall_prediction": readable_label,
        "model_label": overall_label,
        "average_confidence": round(
            average_confidence,
            2
        ),
        "total_chunks": len(results),
        "total_words": len(
            cleaned_text.split()
        ),
        "label_distribution": label_counts,
        "chunks": results
    }


def convert_label(label: str):
    """
    Convert model labels into readable names.

    IMPORTANT:
    The exact label meaning depends on the model.
    """

    label_upper = label.upper()

    if label_upper in [
        "LABEL_1",
        "AI",
        "FAKE"
    ]:
        return "AI-generated / AI-like"

    elif label_upper in [
        "LABEL_0",
        "HUMAN",
        "REAL"
    ]:
        return "Human-written / Human-like"

    return label