import cv2
import numpy as np
import random

def simulate_sun_damage(input_path, output_path):
    try:
        image = cv2.imread(input_path)
        if image is None:
            return False

        height, width, _ = image.shape
        center_x, center_y = width // 2, int(height * 0.55)

        # Approximate full face mask
        face_mask = np.zeros((height, width), dtype=np.uint8)
        axes_length = (int(width * 0.22), int(height * 0.28))
        cv2.ellipse(face_mask, (center_x, center_y), axes_length, 0, 0, 360, 255, -1)

        # Define facial zones (nose bridge, cheeks, forehead)
        zones = [
            (center_x, center_y, 80),  # center face
            (center_x - 60, center_y + 20, 60),  # left cheek
            (center_x + 60, center_y + 20, 60),  # right cheek
            (center_x, center_y - 60, 50),  # forehead
        ]

        output = image.copy()

        for cx, cy, radius in zones:
            num_freckles = random.randint(60, 100)
            for _ in range(num_freckles):
                angle = random.uniform(0, 2 * np.pi)
                r = radius * np.sqrt(random.uniform(0, 1))
                x = int(cx + r * np.cos(angle))
                y = int(cy + r * np.sin(angle))

                if 0 <= x < width and 0 <= y < height and face_mask[y, x] > 0:
                    size = random.randint(1, 3)
                    color = (
                        random.randint(40, 90),  # B
                        random.randint(30, 60),  # G
                        random.randint(20, 40),  # R
                    )
                    cv2.circle(output, (x, y), size, color, -1)

        # Blend only face area
        face_mask_color = cv2.merge([face_mask] * 3)
        final = np.where(face_mask_color > 0, output, image)

        cv2.imwrite(output_path, final)
        return True

    except Exception as e:
        print(f"Simulation failed: {e}")
        return False
