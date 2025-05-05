# 🎨 Aya Palette Backend

This repository is a lightweight Python Flask backend for [Aya](https://github.com/PratikshaDPai/color-palette-cartoonify) that provides two endpoints - one to extract color palettes from an image using KMeans clustering, and one to recolor a base image using a custom palette.

It’s optimized for mobile: images are sent in base64, responses are small, and it works cleanly with my React Native frontend.

Two endpoints are exposed: `/palette` and `/recolor`, and all the processing is done server-side using `Pillow`, `scikit-learn`, and `NumPy`.

This separation of concerns helped me keep the app lightweight and performant on mobile devices

---

## ✨ Features

- ✅ Extract dominant color palettes from images
- ✅ Recolor one image using the palette of another
- ✅ Fast and mobile-friendly API
- ✅ Designed to integrate with a React Native frontend

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/PratikshaDPai/palette-backend.git
cd palette-backend
```

2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the server

```bash
python app.py
```

Server will start on http://127.0.0.1:5000 by default.
📬 API Endpoints
🔹 POST /palette

Extracts a color palette from an image.

Request:

```json
{
  "image": "<base64-encoded-image>"
}
```

Response:

```json
{
  "palette": ["#ab87b1", "#eecc76", "#dd4532", "#f2f2f2", "#222222", "#0099cc"]
}
```

🔹 POST /recolor

Recolors a base image using a custom palette.

Request:

```json
{
  "image": "<base64-encoded-image>",
  "palette": ["#ab87b1", "#eecc76", "#dd4532", "#f2f2f2", "#222222", "#0099cc"]
}
```

Response:

```json
{
  "recolor": "<base64-encoded-PNG>"
}
```

🧠 How It Works
🎯 Palette Extraction

    Resizes input image (128x128) for performance

    Uses KMeans clustering (n=6) to find dominant colors

    Converts cluster centers (RGB) to hex format for frontend use

🎨 Recoloring

    Clusters the base image using KMeans

    Maps each cluster to the closest hex color in the target palette (Euclidean distance in RGB space)

    Reconstructs the image with new colors and returns the result as base64 PNG

📦 Dependencies

    Flask

    Pillow

    NumPy

    scikit-learn

Install all dependencies with:

```bash
pip install -r requirements.txt
```

🧪 Testing with Postman

To test /recolor, provide:

    A base64-encoded image

    A mock palette, like:

["#f311c3", "#0cd5d2", "#dbc722", "#0e5d18", "#ef2a1b", "#0a5ec6"]

📱 Companion Frontend

Check out the frontend repo:

👉 [Aya React Native App](https://github.com/PratikshaDPai/color-palette-cartoonify)
