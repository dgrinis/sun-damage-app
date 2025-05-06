import cv2
import numpy as np

def simulate_sun_damage(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found or unreadable:", image_path)

    # Convert to float for manipulation
    image = image.astype(np.float32) / 255.0

    # Simulate increased redness (add red tint)
    red_channel = image[:, :, 2]
    red_channel = np.clip(red_channel + 0.2, 0, 1)  # Add redness
    image[:, :, 2] = red_channel

    # Simulate contrast boost
    image = np.clip(1.2 * image - 0.1, 0, 1)

    # Convert back to uint8
    simulated = (image * 255).astype(np.uint8)

    # Save the image
    cv2.imwrite(output_path, simulated)
