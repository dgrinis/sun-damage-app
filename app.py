
from flask import Flask, request, send_file
import cv2
import numpy as np
import mediapipe as mp
import os
from PIL import Image, ImageEnhance
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

mp_face_detection = mp.solutions.face_detection

def simulate_sun_damage(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    pil_img = Image.fromarray(img_rgb)

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(img_rgb)
        if not results.detections:
            return None

        damaged = pil_img.copy()
        draw = ImageEnhance.Contrast(damaged).enhance(1.5)
        draw_np = np.array(draw)

        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            x, y = int(bbox.xmin * w), int(bbox.ymin * h)
            box_w, box_h = int(bbox.width * w), int(bbox.height * h)

            for _ in range(200):
                cx = np.random.randint(x, x + box_w)
                cy = np.random.randint(y, y + box_h)
                radius = np.random.randint(1, 3)
                color = (np.random.randint(90, 120), np.random.randint(60, 80), np.random.randint(50, 70))
                cv2.circle(draw_np, (cx, cy), radius, color, -1)

        result_img = Image.fromarray(draw_np)
        out_path = os.path.join(OUTPUT_FOLDER, f"out_{uuid.uuid4().hex}.jpg")
        result_img.save(out_path)
        return out_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        result_path = simulate_sun_damage(filepath)
        if result_path is None:
            return 'No face detected.', 400

        return send_file(result_path, mimetype='image/jpeg')

    return '''
    <!doctype html>
    <title>Sun Damage Simulator</title>
    <h1>Upload a Selfie</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=10000)

