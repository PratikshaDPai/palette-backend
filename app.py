# app.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

def get_palette_from_image(img, n_colors=6):
    # Resize for faster processing
    img = cv2.resize(img, (100, 100))
    img = img.reshape((-1, 3))

    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(img)

    colors = np.array(kmeans.cluster_centers_, dtype='uint8')
    hex_colors = ['#%02x%02x%02x' % tuple(c) for c in colors]
    return hex_colors

@app.route("/palette", methods=["POST"])
def extract_palette():
    data = request.json
    if "image" not in data:
        return jsonify({"error": "No image found"}), 400

    # Decode base64 image
    try:
        base64_data = base64.b64decode(data["image"])
        image = Image.open(BytesIO(base64_data)).convert("RGB")
        img_array = np.array(image)
        palette = get_palette_from_image(img_array)
        return jsonify({"palette": palette})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
