import cv2

def simulate_sun_damage(input_path, output_path):
    image = cv2.imread(input_path)
    if image is None:
        return False  # No image found or bad input

    # Dummy simulation: convert to grayscale
    result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, result)
    return True
