import face_recognition
import numpy as np
import base64
from PIL import Image


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
