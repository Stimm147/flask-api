import torch
import torchvision.transforms as transforms
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small
from PIL import Image
import requests
from fastapi import FastAPI




class ImageClassifier:
    LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"

    def __init__(self):
        pass

    def fetch_model(self):
        model = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT)
        model.eval()
        return model

    def classify_image(self, data):
        transform = transforms.Compose(
            [
                transforms.Resize(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        MODEL = self.fetch_model()

        imagenet_labels = requests.get(self.LABELS_URL).json()

        image = Image.open(data)

        output = MODEL(transform(image).unsqueeze(0))
        prediction = torch.argmax(output).item()
        confidence = torch.softmax(output, 1).max().item()

        return {
            "class_id": prediction,
            "class_name": imagenet_labels[prediction],
            "confidence": round(confidence * 100, 1),
        }

app = FastAPI()

classifier = ImageClassifier()

@app.post("/")
def classify(data: dict):
    img_url = data["url"]
    downloaded_img = requests.get(img_url, stream=True).raw
    result = classifier.classify_image(data=downloaded_img)
    return result