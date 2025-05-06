import cv2
import numpy as np
import mediapipe as mp

def apply_extreme_sun_damage(image_path, output_path):
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return False

        # Convert to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Face detection
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            return False

        # Create mask
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        h, w = mask.shape

        for face_landmarks in results.multi_face_landmarks:
            points = [(int(landmark.x * w), int(landmark.y * h)) for landmark in face_landmarks.landmark]
            hull = cv2.convexHull(np.array(points))
            cv2.drawContours(mask, [hull], -1, 255, -1)

        # Add noise to simulate extreme sun damage
        noise = np.random.normal(loc=30, scale=50, size=image.shape).astype(np.uint8)
        damaged = cv2.add(image, noise)

        # Blur and darken
        damaged = cv2.GaussianBlur(damaged, (7, 7), 0)
        damaged = cv2.addWeighted(damaged, 0.6, image, 0.4, 0)

        # Only apply to face region
        face_only = cv2.bitwise_and(damaged, damaged, mask=mask)
        background = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
        final = cv2.add(face_only, background)

        # Save result
        cv2.imwrite(output_path, final)
        return True

    except Exception as e:
        print(f"Simulation error: {e}")
        return False

# Adapter function for Flask app

def simulate_sun_damage(image_path, output_path):
    return apply_extreme_sun_damage(image_path, output_path)
