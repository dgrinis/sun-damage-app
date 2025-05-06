import cv2
import numpy as np

def simulate_sun_damage(input_path, output_path):
    try:
        # Load original image
        image = cv2.imread(input_path)
        if image is None:
            return False

        # Convert to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Simulate freckles / sunspots using noise
        noise = np.random.normal(loc=0.5, scale=0.5, size=image_rgb.shape[:2])
        noise = cv2.GaussianBlur(noise, (9, 9), 0)
        freckle_mask = np.uint8((noise * 255).clip(0, 255))

        # Create a brown color map to overlay as spots
        brown = np.full_like(image_rgb, (90, 60, 30))
        freckle_colored = cv2.bitwise_and(brown, brown, mask=freckle_mask)

        # Blend freckles with original
        freckles_layer = cv2.addWeighted(image_rgb, 1, freckle_colored, 0.2, 0)

        # Add aging: reduce brightness slightly and increase contrast
        contrasted = cv2.convertScaleAbs(freckles_layer, alpha=1.3, beta=-30)

        # Slight blur for weathered look
        final = cv2.GaussianBlur(contrasted, (3, 3), 0)

        # Convert back to BGR for saving
        final_bgr = cv2.cvtColor(final, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, final_bgr)

        return True

    except Exception as e:
        print("Error:", e)
        return False
