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
    
@app.route('/recolor',methods=['POST'])
def recolor_image():
    data=request.json
    base64_str = data['image']
    palette=data['palette']

    if not palette:
        return jsonify({"error": "Palette is empty"}), 400

    #decode base64, same as palette extractor
    img_data= base64.b64decode(base64_str)
    img=Image.open(BytesIO(img_data)).convert('RGB')
    img_np=np.array(img)

    #Reshape to (n_pixels,3)
    pixels = img_np.reshape(-1, 3)

    # Cluster image pixels
    num_clusters = max(1, min(len(palette), 5))
    kmeans = KMeans(n_clusters=num_clusters, n_init=10)
    labels = kmeans.fit_predict(pixels)
    clustered = kmeans.cluster_centers_.astype(np.uint8)

    # Convert hex palette to RGB
    hex_to_rgb = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
    target_colors = np.array([hex_to_rgb(h) for h in palette], dtype=np.uint8)

    # Map each cluster to the closest target color
    recolor_map = {}
    for i, c in enumerate(clustered):
        distances = np.linalg.norm(target_colors - c, axis=1)
        recolor_map[i] = target_colors[np.argmin(distances)]

    # Apply recoloring
    new_pixels = np.array([recolor_map[l] for l in labels], dtype=np.uint8)
    new_img_np = new_pixels.reshape(img_np.shape)

    # Encode back to base64
    recolored_img = Image.fromarray(new_img_np)
    buffered = BytesIO()
    recolored_img.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({"recolor": encoded})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
