from ddgs import DDGS
import os
import re
import requests

IMAGE_FOLDER = "static/images"

os.makedirs(IMAGE_FOLDER, exist_ok=True)


def get_image(laptop_name):

    filename = re.sub(r'[^a-zA-Z0-9]', '_', laptop_name.lower()) + ".jpg"
    filepath = os.path.join(IMAGE_FOLDER, filename)

    # Agar image pehle se download hai to wahi use karo
    if os.path.exists(filepath):
        return f"https://laptop-recommendation-api.onrender.com/static/images/{filename}"

    with DDGS() as ddgs:
        results = list(
            ddgs.images(
                f"{laptop_name} laptop",
                max_results=5
            )
        )

    if not results:
        return None

    image_url = None

    for result in results:
        title = result.get("title", "").lower()
        url = result.get("image", "").lower()

        bad_words = [
        "wallpaper", "person", "people", "anime",
        "logo", "icon", "avatar", "pumpkin"
        ]

        if any(word in title or word in url for word in bad_words):
          continue

        image_url = result["image"]
        break

    if image_url is None:
       image_url = results[0]["image"]

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            image_url,
            headers=headers,
            timeout=10
        )

        content_type = response.headers.get("Content-Type", "")

        if response.status_code == 200 and content_type.startswith("image/"):
            with open(filepath, "wb") as f:
                f.write(response.content)

            return f"https://laptop-recommendation-api.onrender.com/static/images/{filename}"

    except Exception as e:
        print(e)

    return None