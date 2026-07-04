from ddgs import DDGS
import os
import re
import requests


IMAGE_FOLDER = "static/images"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

def clear_old_images():

    for file in os.listdir(IMAGE_FOLDER):

        file_path = os.path.join(IMAGE_FOLDER, file)

        if os.path.isfile(file_path):
            os.remove(file_path)

def get_image(laptop_name):

    filename = re.sub(r'[^a-zA-Z0-9]', '_', laptop_name.lower()) + ".jpg"
    filepath = os.path.join(IMAGE_FOLDER, filename)

    # Agar image pehle se download hai
    if os.path.exists(filepath):
        return f"https://laptop-recommendation-api.onrender.com/static/images/{filename}"

    with DDGS() as ddgs:
     results = list(
        ddgs.images(
            f"{laptop_name} laptop",
            max_results=1
        )
    )

    if not results:
      return None

    image_url = results[0]["image"]

    try:
        headers = {
        "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(image_url, timeout=10,headers=headers)

        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)

            return f"https://laptop-recommendation-api.onrender.com/static/images/{filename}"

    except Exception as e:
        print(e)

    return None