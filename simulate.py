import cv2
import numpy as np
import mediapipe as mp

def simulate_sun_damage(input_path, output_path):
    try:
        image = cv2.imread(input_path)
        if image is None:
            return False

        mp_face_mesh = mp.solutions.face_mesh
        mp_drawing = mp.solutions.drawing_utils

        with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.multi_face_landmarks:
                return False

            h, w, _ = image.shape
            mask = np.zeros((h, w), dtype=np.uint8)

            for face_landmarks in results.multi_face_landmarks:
                points = []
                for lm in face_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    points.append((x, y))
                points = np.array(points, dtype=np.int32)
                cv2.fillConvexPoly(mask, points, 255)

            # Create simulated freckles as noise
            noise = np.random.normal(loc=0, scale=255, size=image.shape).astype(np.uint8)
            sun_damage = cv2.addWeighted(image, 1, noise, 0.07, 0)

            # Apply noise only to face mask
            result = image.copy()
            for c in range(3):
                result[:, :, c] = np.where(mask == 255, sun_damage[:, :, c], image[:, :, c])

            cv2.imwrite(output_path, result)
            return True

    except Exception as e:
        print("Simulation error:", e)
        return False
