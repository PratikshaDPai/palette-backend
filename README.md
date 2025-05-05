# 🎨 Aya Palette Backend

This repository is a lightweight Python Flask backend for [Aya](https://github.com/PratikshaDPai/color-palette-cartoonify) that provides two endpoints - one to extract color palettes from an image using KMeans clustering, and one to recolor a base image using a custom palette.

It’s optimized for mobile: images are sent in base64, responses are small, and it works cleanly with my React Native frontend.

Two endpoints are exposed: `/palette` and `/recolor`, and all the processing is done server-side using `Pillow`, `scikit-learn`, and `NumPy`.

This separation of concerns helped me keep the app lightweight and performant on mobile devices

---

## Features

-  Extract dominant color palettes from images
-  Recolor a base image using a provided palette
-  Fast and mobile-friendly APIs
-  Designed to integrate with a React Native frontend

---

## 🧩 Backend Logic

### /palette – Extract a Color Palette
Purpose: Take a user-uploaded image (base64) → return its 6 most dominant colors

  How:
- Resize the image to 100×100 (speeds up processing)
- Flatten the image into a list of pixels (RGB values)
- Apply KMeans(n=6) from sklearn.cluster
- Convert the RGB cluster centers to hex codes like #aabbcc
- Return the list of hex codes in a JSON response

### /recolor – Recolor the Base Image
Purpose: Replace the base image’s color clusters with new palette colors

  How:
- Decode the base64 image and convert it to a NumPy array
- Resize if it's too large (>2000px on any side) to keep memory low
- Flatten the image into pixels and sample every 5th pixel to speed things up
- Run MiniBatchKMeans to cluster the image pixels
- For each cluster center, find the closest palette color using Euclidean RGB distance
- Replace every pixel’s cluster with its corresponding palette color
- Reconstruct the image → encode as base64 → return to frontend

## Using the Repository

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
## API Endpoints
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

##  Testing with Postman

To test /recolor, provide:

    A base64-encoded image

    A mock palette, like:

["#f311c3", "#0cd5d2", "#dbc722", "#0e5d18", "#ef2a1b", "#0a5ec6"]

## 📱 Companion Frontend

Check out the frontend repo:

 [Aya React Native App](https://github.com/PratikshaDPai/color-palette-cartoonify)
