import cv2
import numpy as np
import traceback

def simulate_sun_damage(image_path, output_path):
    try:
        # Load the original image
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image at: {image_path}")

        # Convert to YUV color space to work on brightness
        yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

        # Decrease brightness (simulate long-term UV exposure)
        yuv[:, :, 0] = np.clip(yuv[:, :, 0] * 0.8, 0, 255)  # Y channel controls brightness

        # Convert back to BGR
        simulated = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

        # Optional: add freckles or increase contrast if desired

        # Save the processed image
        success = cv2.imwrite(output_path, simulated)
        if not success:
            raise IOError(f"Failed to write image to: {output_path}")

        return True  # Indicate success
    except Exception as e:
        print("❌ Simulation failed:", str(e))
        traceback.print_exc()
        return False  # Indicate failure
