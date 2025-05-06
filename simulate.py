import cv2
import numpy as np
import traceback

def simulate_sun_damage(image_path, output_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image at: {image_path}")

        # Step 1: Slightly increase contrast
        image = cv2.convertScaleAbs(image, alpha=1.3, beta=-20)  # alpha > 1.0 = more contrast

        # Step 2: Convert to HSV and boost reds (freckles/sun damage tones)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = np.clip(s + 20, 0, 255)  # Boost saturation
        v = np.clip(v - 10, 0, 255)  # Slightly darken
        hsv = cv2.merge([h, s, v])
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Step 3: Add subtle speckle noise (simulate texture)
        noise = np.random.normal(0, 8, image.shape).astype(np.uint8)
        image = cv2.add(image, noise)

        # Step 4: Save result
        success = cv2.imwrite(output_path, image)
        if not success:
            raise IOError(f"Could not write image to: {output_path}")

        return True
    except Exception as e:
        print("❌ Simulation failed:", str(e))
        traceback.print_exc()
        return False
