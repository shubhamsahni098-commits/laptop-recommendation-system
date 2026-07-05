from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation import recommend_laptops
import os
import time
import random

app = Flask(__name__)
CORS(app)

IMAGES = [
    "https://laptop-recommendation-api.onrender.com/static/images/laptop1.png",
    "https://laptop-recommendation-api.onrender.com/static/images/laptop2.png",
    "https://laptop-recommendation-api.onrender.com/static/images/laptop3.png",
    "https://laptop-recommendation-api.onrender.com/static/images/laptop4.png",
    "https://laptop-recommendation-api.onrender.com/static/images/laptop5.png",
]


@app.route("/")
def home():
    return "Laptop Recommendation API Running"


@app.route("/recommend", methods=["POST"])
def recommend():
    time.sleep(3)

    data = request.get_json()

    budget = data["budget"]
    primary_use = data["primary_use"]
    secondary_use = data.get("secondary_use")

    result = recommend_laptops(
        budget,
        primary_use,
        secondary_use
    )

    if isinstance(result, list):
        images = IMAGES.copy()
        random.shuffle(images)

        for i, laptop in enumerate(result):
            laptop["image"] = images[i % len(images)]

    return jsonify(result)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )