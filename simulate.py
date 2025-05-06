import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os

def simulate_sun_damage(input_path, output_path):
    try:
        # Load and enhance image contrast
        image = cv2.imread(input_path)
        if image is None:
            return False

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        contrast = ImageEnhance.Contrast(pil_image).enhance(2.2)
        enhanced = cv2.cvtColor(np.array(contrast), cv2.COLOR_RGB2BGR)

        # Detect faces
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        # Apply darker freckle-like dots in face region
        for (x, y, w, h) in faces:
            for _ in range(1500):
                rx = np.random.randint(x, x + w)
                ry = np.random.randint(y, y + h)
                cv2.circle(enhanced, (rx, ry), radius=1, color=(30, 30, 30), thickness=-1)

        # Save result
        cv2.imwrite(output_path, enhanced)
        return True

    except Exception as e:
        print("Sun damage simulation failed:", e)
        return False
