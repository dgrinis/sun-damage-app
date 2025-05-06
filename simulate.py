import cv2
import os
import uuid

def simulate_sun_damage(image_path):
    # Read the uploaded image
    image = cv2.imread(image_path)
    if image is None:
        return None

    # Simulate "sun damage" by increasing contrast and adding a reddish filter
    damage = cv2.convertScaleAbs(image, alpha=1.5, beta=20)
    damage[:, :, 2] = cv2.add(damage[:, :, 2], 30)  # Boost red channel

    # Generate a unique filename for the result
    result_filename = f"{uuid.uuid4().hex}.jpg"
    result_path = os.path.join('static/results', result_filename)

    # Save the processed image
    cv2.imwrite(result_path, damage)

    return result_path
