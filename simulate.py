from PIL import Image, ImageDraw, ImageEnhance
import numpy as np
import cv2

def apply_extreme_sun_damage(image_path, output_path):
    # Load image
    original = Image.open(image_path).convert("RGB")
    image_np = np.array(original)

    # Convert to OpenCV format
    img_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Detect face using Haar cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        original.save(output_path)
        return False

    # Convert back to PIL
    damaged = original.copy()
    draw = ImageDraw.Draw(damaged)

    for (x, y, w, h) in faces:
        # Create freckles
        for _ in range(500):
            fx = np.random.randint(x, x + w)
            fy = np.random.randint(y, y + h)
            r = np.random.randint(1, 3)
            draw.ellipse((fx, fy, fx + r, fy + r), fill=(75, 45, 30, 180))

        # Create patchy sunspots
        for _ in range(100):
            px = np.random.randint(x, x + w)
            py = np.random.randint(y, y + h)
            pr = np.random.randint(8, 15)
            color = (90 + np.random.randint(30), 60, 40)
            draw.ellipse((px, py, px + pr, py + pr), fill=color)

    # Apply uneven contrast and warmth
    enhancer_contrast = ImageEnhance.Contrast(damaged)
    damaged = enhancer_contrast.enhance(1.2)

    enhancer_color = ImageEnhance.Color(damaged)
    damaged = enhancer_color.enhance(1.3)

    enhancer_brightness = ImageEnhance.Brightness(damaged)
    damaged = enhancer_brightness.enhance(0.95)

    # Save result
    damaged.save(output_path)
    return True
