import cv2
import numpy as np
import mediapipe as mp
import random

def simulate_sun_damage(image_path, output_path, intensity=0.6):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        return False

    h, w, _ = image.shape

    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

    # Convert image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if not results.multi_face_landmarks:
        return False

    # Create face mask
    mask = np.zeros((h, w), dtype=np.uint8)
    face_landmarks = results.multi_face_landmarks[0]
    points = [(int(p.x * w), int(p.y * h)) for p in face_landmarks.landmark]
    hull = cv2.convexHull(np.array(points))
    cv2.fillConvexPoly(mask, hull, 255)

    # Generate fake sun damage (freckles/age spots) within the face mask
    freckle_count = int(500 * intensity)
    for _ in range(freckle_count):
        for _ in range(5):  # Retry if random point isn't on the face
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            if mask[y, x] > 0:
                radius = random.randint(1, 3)
                color = (
                    random.randint(20, 40),  # Blue-ish
                    random.randint(30, 60),  # Green-ish
                    random.randint(50, 80)   # Red-ish — brownish overall
                )
                cv2.circle(image, (x, y), radius, color, -1)
                break

    # Save result
    cv2.imwrite(output_path, image)
    return True
