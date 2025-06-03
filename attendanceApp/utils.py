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
            return base64.b64encode(encodings[0]).decode('utf-8')
    except Exception as e:
        print(f"Face encoding error: {e}")

    return None


def match_employee_by_selfie(selfie_image_file, known_employees):
    """
    Given a selfie image file and a queryset of employees with stored encodings,
    return the matching Employee instance or None.
    """
    try:
        selfie_image = Image.open(selfie_image_file).convert(
            'RGB').resize((500, 500))
        selfie_array = np.array(selfie_image)
        selfie_encodings = face_recognition.face_encodings(selfie_array)

        if not selfie_encodings:
            print("No face found in selfie.")
            return None

        selfie_encoding = selfie_encodings[0]

        for employee in known_employees:
            if not employee.photo_encoding:
                continue
            try:
                employee_encoding = np.frombuffer(base64.b64decode(
                    employee.photo_encoding), dtype=np.float64)
                match = face_recognition.compare_faces(
                    [employee_encoding], selfie_encoding)[0]
                if match:
                    print(f"Matched with: {employee.name}")
                    return employee
            except Exception as e:
                print(f"Error decoding face for employee {employee.id}: {e}")

    except Exception as e:
        print(f"Error processing selfie: {e}")
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
