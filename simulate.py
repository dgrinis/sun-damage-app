import cv2
import os

def simulate_sun_damage(image_path):
    # Read the image
    img = cv2.imread(image_path)

    if img is None:
        return None

    # Copy the image to avoid modifying original
    sun_damage = img.copy()

    # Simulate sun damage by enhancing the red channel slightly
    sun_damage[:, :, 2] = cv2.add(sun_damage[:, :, 2], 30)  # Red channel

    # Save the result to 'static/results' with the same filename
    filename = os.path.basename(image_path)
    result_path = os.path.join("static/results", filename)
    cv2.imwrite(result_path, sun_damage)

    return result_path
