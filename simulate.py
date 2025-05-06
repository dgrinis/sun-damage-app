import cv2
import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

def simulate_sun_damage(input_path, output_path):
    try:
        image = cv2.imread(input_path)
        if image is None:
            print("Failed to read image")
            return False

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
            results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            print("No face landmarks detected")
            return False

        # Create face mask
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        h, w = image.shape[:2]
        for landmarks in results.multi_face_landmarks:
            points = []
            for lm in landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                points.append((x, y))
            hull = cv2.convexHull(np.array(points))
            cv2.fillConvexPoly(mask, hull, 255)

        # Generate freckle-like noise
        damage_layer = np.zeros_like(image, dtype=np.uint8)
        freckle_count = 600
        for _ in range(freckle_count):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            if mask[y, x] > 0:
                radius = np.random.randint(1, 3)
                intensity = np.random.randint(40, 90)
                cv2.circle(damage_layer, (x, y), radius, (intensity, intensity, intensity), -1)

        # Blend freckles into face only
        face_area = cv2.bitwise_and(image, image, mask=mask)
        freckled = cv2.addWeighted(face_area, 1, damage_layer, 0.6, 0)
        result = image.copy()
        result[mask > 0] = freckled[mask > 0]

        cv2.imwrite(output_path, result)
        return True

    except Exception as e:
        print(f"Error during simulation: {e}")
        return False
