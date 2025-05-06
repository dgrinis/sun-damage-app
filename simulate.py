import cv2

def simulate_sun_damage(input_path, output_path):
    try:
        image = cv2.imread(input_path)
        if image is None:
            return False

        # Apply basic grayscale filter as a placeholder
        simulated = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        simulated = cv2.cvtColor(simulated, cv2.COLOR_GRAY2BGR)

        cv2.imwrite(output_path, simulated)
        return True
    except Exception as e:
        print(f"Error simulating sun damage: {e}")
        return False
