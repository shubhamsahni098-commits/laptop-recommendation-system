from flask import Flask, request, jsonify
from image_search import get_image, clear_old_images
from flask_cors import CORS
import time
from recommendation import recommend_laptops

app = Flask(__name__)
CORS(app)


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

    clear_old_images()
    result = recommend_laptops(
        budget,
        primary_use,
        secondary_use
    )
    if isinstance(result, list):
     for laptop in result:
        laptop["image"] = get_image(laptop["name"])

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)