import cv2
import numpy as np
import os

def simulate_sun_damage(image_path, output_path):
    try:
        # Load image
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Failed to load image from: {image_path}")

        # Convert to float for processing
        image = image.astype(np.float32) / 255.0

        # Add red tint (sun damage effect)
        image[:, :, 2] = np.clip(image[:, :, 2] + 0.2, 0, 1)

        # Increase contrast
        image = np.clip(1.2 * image - 0.1, 0, 1)

        # Convert back to uint8
        simulated = (image * 255).astype(np.uint8)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the result
        success = cv2.imwrite(output_path, simulated)
        if not success:
            raise IOError(f"Failed to write image to: {output_path}")

    except Exception as e:
        print("❌ Simulation failed:", str(e))
        raise
