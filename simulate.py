import cv2
import numpy as np

def simulate_sun_damage(input_path, output_path):
    try:
        # Load and convert to RGB
        image = cv2.imread(input_path)
        if image is None:
            return False
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Generate strong noise mask for dark spots
        noise = np.random.normal(loc=0.3, scale=1.2, size=image_rgb.shape[:2])
        noise = cv2.GaussianBlur(noise, (7, 7), 0)
        noise_mask = np.clip(noise * 255, 0, 255).astype(np.uint8)

        # Threshold for visible dark freckles
        _, binary_mask = cv2.threshold(noise_mask, 120, 255, cv2.THRESH_BINARY)

        # Freckle color (darker brown)
        freckle_color = np.full_like(image_rgb, (60, 40, 20))  # RGB
        freckle_layer = cv2.bitwise_and(freckle_color, freckle_color, mask=binary_mask)

        # Overlay stronger freckles
        damaged = cv2.addWeighted(image_rgb, 1, freckle_layer, 0.7, 0)

        # Apply mild yellow tint (sun discoloration)
        yellow_filter = np.full_like(damaged, (30, 20, 0))  # light brown
        damaged = cv2.addWeighted(damaged, 0.9, yellow_filter, 0.3, 5)

        # Increase contrast and lower brightness for more drama
        damaged = cv2.convertScaleAbs(damaged, alpha=1.5, beta=-40)

        # Optional: slight blur to simulate aging texture
        damaged = cv2.GaussianBlur(damaged, (3, 3), 0)

        # Save the result
        result_bgr = cv2.cvtColor(damaged, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, result_bgr)
        return True

    except Exception as e:
        print("Simulation error:", e)
        return False
