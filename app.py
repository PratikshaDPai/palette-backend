# app.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
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
    
@app.route('/recolor', methods=['POST'])
def recolor_image():
    try:
        data = request.get_json(force=True)
        base64_str = data.get('image')
        palette = data.get('palette')

        if not base64_str or not palette:
            print("Missing image or palette:", data)
            return jsonify({"error": "Missing image or palette"}), 400

        # Decode and convert to RGB
        img_data = base64.b64decode(base64_str)
        img = Image.open(BytesIO(img_data)).convert('RGB')

        # Resize if needed (preserve aspect ratio)
        max_dim = 2000
        if max(img.size) > max_dim:
            w, h = img.size
            if w > h:
                new_w = max_dim
                new_h = int(h * max_dim / w)
            else:
                new_h = max_dim
                new_w = int(w * max_dim / h)
            img = img.resize((new_w, new_h))

        img_np = np.array(img)
        pixels = img_np.reshape(-1, 3)

        # Sample every 5th pixel to speed up clustering
        sample_pixels = pixels[::5]

        # Cluster sampled pixels
        num_clusters = max(1, min(len(palette), 5))
        kmeans = MiniBatchKMeans(n_clusters=num_clusters, batch_size=1024, n_init=3)
        labels = kmeans.fit_predict(pixels)  # full image
        clustered = kmeans.cluster_centers_.astype(np.uint8)

        # Convert hex palette to RGB
        hex_to_rgb = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
        target_colors = np.array([hex_to_rgb(h) for h in palette], dtype=np.uint8)

        # Map each cluster to closest palette color
        recolor_map = {}
        for i, c in enumerate(clustered):
            distances = np.linalg.norm(target_colors - c, axis=1)
            recolor_map[i] = target_colors[np.argmin(distances)]

        # Apply recoloring
        new_pixels = np.array([recolor_map[l] for l in labels], dtype=np.uint8)
        new_img_np = new_pixels.reshape(img_np.shape)

        # Encode final image
        recolored_img = Image.fromarray(new_img_np)
        buffered = BytesIO()
        recolored_img.save(buffered, format="PNG")
        encoded = base64.b64encode(buffered.getvalue()).decode()

        print("Recolor success.")
        return jsonify({"recolor": encoded})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Server crash", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
