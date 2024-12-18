import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image


model_name = "jolual2747/vit-clothes-classification"
processor = AutoImageProcessor.from_pretrained(model_name)
clothes_classification_model = AutoModelForImageClassification.from_pretrained(model_name)


def classify_clothes(image_path) -> str:
    image = Image.open(image_path)
    image = image.convert("RGB")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        logits = clothes_classification_model(**inputs).logits

    predicted_class = logits.argmax(-1).item()

    labels = clothes_classification_model.config.id2label

    return labels[predicted_class]
