# Utility functions for face recognition and attendance management
# These functions handle encoding images, matching faces, and calculating attendance hours.
# They are designed to work with Django models and image files.
## Note: Ensure you have the required libraries installed:
# pip install face_recognition numpy Pillow
# Also, ensure you have the necessary face_recognition model files available in your environment.
# Usage of these functions assumes you have a Django model with an ImageField for employee photos
# and a field to store the base64 encoded face encodings.

import face_recognition
import numpy as np
import base64
from PIL import Image
from datetime import datetime, timedelta


def encode_face_from_image_file(image_file) -> str | None:
    """
    Given an image file (e.g., from ImageField or UploadedFile),
    process and return a base64 encoded face encoding string.

    Returns None if no face encoding is found or on error.
    """
    try:
        # Open image, convert to RGB and resize for consistent processing
        image = Image.open(image_file).convert('RGB').resize((500, 500))
        image_array = np.array(image)

        encodings = face_recognition.face_encodings(image_array)
        if encodings:
            # Encode as base64 string for storage
            return base64.b64encode(encodings[0].tobytes()).decode('utf-8')
    except Exception as e:
        print(f"Face encoding error: {e}")

    return None


def match_employee_by_selfie(selfie_image_file, known_employees):
    """
    Attempts to match a selfie image against known employee encodings.
    Returns the matched employee object or None if no match is found.
    """
    # Match threshold (tunable)
    threshold = 0.4

    try:
        selfie_image = Image.open(selfie_image_file).convert('RGB').resize((500, 500))
        selfie_array = np.array(selfie_image)
        selfie_encodings = face_recognition.face_encodings(selfie_array)

        if not selfie_encodings:
            print("❗ No face found in selfie.")
            return None

        selfie_encoding = selfie_encodings[0]

        for employee in known_employees:
            if not employee.photo_encoding:
                print(f"⚠️ Skipping employee {employee.employeeCode} ({employee.name}): No encoding available.")
                continue

            try:
                # Decode stored base64-encoded face embedding
                employee_encoding = np.frombuffer(
                    base64.b64decode(employee.photo_encoding), dtype=np.float64)

                distance = face_recognition.face_distance([employee_encoding], selfie_encoding)[0]
                is_match = face_recognition.compare_faces(
                    [employee_encoding], selfie_encoding, tolerance=threshold)[0]

                confidence = max(0, (1 - distance / threshold)) * 100

                print(f"🔍 {employee.employeeCode} ({employee.name}) → Distance: {distance:.4f} → Confidence: {confidence:.2f}%, Match: {is_match}")

                if is_match:
                    print(f"✅ Matched with: ({employee.employeeCode}, {employee.name})")
                    return employee

            except Exception as e:
                print(f"❌ Error decoding or comparing face for employee {employee.employeeCode}: {e}")

    except Exception as e:
        print(f"❌ Error processing selfie: {e}")

    print("🚫 No matching employee found.")
    return None




def compute_total_hours(time_in, time_out):
    # Assume same day for now
    today = datetime.today().date()
    dt_in = datetime.combine(today, time_in)
    dt_out = datetime.combine(today, time_out)

    # If time_out is before time_in (e.g., overnight shift), adjust date
    if dt_out < dt_in:
        dt_out += timedelta(days=1)

    duration = dt_out - dt_in
    total_hours = round(duration.total_seconds() / 3600, 2)  # hours as float
    return total_hours
