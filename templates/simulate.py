import cv2
import os

def simulate_sun_damage(input_path):
    image = cv2.imread(input_path)
    if image is None:
        return None

    # Simple simulated effect: darken with a red tint
    overlay = image.copy()
    overlay[:] = (0, 0, 100)  # Red-ish overlay

    simulated = cv2.addWeighted(image, 0.6, overlay, 0.4, 0)

    output_path = input_path.replace("uploads", "results")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, simulated)

    return output_path
