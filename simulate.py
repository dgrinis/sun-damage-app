import cv2
import numpy as np

def simulate_sun_damage(input_path, output_path):
    try:
        # Load image
        image = cv2.imread(input_path)
        if image is None:
            return False

        height, width, _ = image.shape

        # Create an elliptical mask for the face region
        mask = np.zeros((height, width), dtype=np.uint8)
        center_x, center_y = width // 2, height // 2
        axes_length = (width // 4, height // 3)
        cv2.ellipse(mask, (center_x, center_y), axes_length, 0, 0, 360, 255, -1)

        # Convert mask to 3-channel
        mask_color = cv2.merge([mask, mask, mask])

        # Create noise for sun damage
        noise = np.random.normal(loc=0, scale=60, size=image.shape).astype(np.int16)
        noise_masked = (noise * (mask_color > 0)).astype(np.int16)

        # Add noise to the image
        damaged_image = image.astype(np.int16) + noise_masked
        damaged_image = np.clip(damaged_image, 0, 255).astype(np.uint8)

        # Blend the original image and damaged image using the mask
        output = np.where(mask_color > 0, damaged_image, image)

        # Save the result
        cv2.imwrite(output_path, output)
        return True

    except Exception as e:
        print(f"Error in simulate_sun_damage: {e}")
        return False
