from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2
from PIL import Image
import requests

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {"origins": "https://portfolio-production-3beb.up.railway.app"}
    },
)

model = mobilenet_v2(pretrained=True)
model.eval()

transform = transforms.Compose(
    [
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


@app.route("/api/classify", methods=["POST"])
def classify():
    try:
        url = request.json["url"]
        image = Image.open(requests.get(url, stream=True).raw)

        with torch.no_grad():
            output = model(transform(image).unsqueeze(0))
            prediction = torch.argmax(output).item()
            confidence = torch.softmax(output, 1).max().item()

        return jsonify(
            {"class_id": prediction, "confidence": round(confidence * 100, 1)}
        )
    except:
        return jsonify({"error": "Failed"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5001)
