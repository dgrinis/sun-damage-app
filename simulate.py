import cv2
import numpy as np
import random

def simulate_sun_damage(input_path, output_path):
    try:
        image = cv2.imread(input_path)
        if image is None:
            return False

        height, width, _ = image.shape

        # Create elliptical mask for face approximation
        face_mask = np.zeros((height, width), dtype=np.uint8)
        center_x, center_y = width // 2, int(height * 0.55)
        axes_length = (int(width * 0.22), int(height * 0.28))
        cv2.ellipse(face_mask, (center_x, center_y), axes_length, 0, 0, 360, 255, -1)

        # Convert to color mask for blending
        face_mask_color = cv2.merge([face_mask] * 3)

        # Copy the original image to draw freckles
        simulated = image.copy()

        # Parameters for freckle simulation
        num_freckles = 300
        for _ in range(num_freckles):
            # Random point within ellipse
            x = random.randint(center_x - axes_length[0], center_x + axes_length[0])
            y = random.randint(center_y - axes_length[1], center_y + axes_length[1])

            if face_mask[y, x] > 0:
                radius = random.randint(1, 2)
                intensity = random.randint(30, 60)
                color = (intensity, intensity // 2, intensity // 3)  # light brown
                cv2.circle(simulated, (x, y), radius, color, -1)

        # Blend the simulated damage only where mask is applied
        output = np.where(face_mask_color > 0, simulated, image)

        # Save final result
        cv2.imwrite(output_path, output)
        return True

    except Exception as e:
        print(f"Sun damage simulation failed: {e}")
        return False
