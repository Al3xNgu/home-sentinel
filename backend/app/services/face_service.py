from deepface import DeepFace

MIN_FACE_CONFIDENCE = 0.90

def detect_faces(image_path: str):
    faces = DeepFace.extract_faces(
        img_path=image_path,
        detector_backend="opencv",
        enforce_detection=False
    )

    confident_faces = [
        face for face in faces
        if face.get("confidence", 0) >= MIN_FACE_CONFIDENCE
    ]

    return confident_faces

def validate_single_face(image_path: str):
    faces = detect_faces(image_path)

    if len(faces) == 0:
        return False, "No face detected"

    if len(faces) > 1:
        return False, "Multiple faces detected"

    return True, None