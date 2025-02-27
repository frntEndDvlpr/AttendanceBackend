from rest_framework import serializers
from .models import Employee, PhotoLibrary, AttendanceLog, Project
import face_recognition
import numpy as np
import base64
from PIL import Image
import io

def encode_face(image):
    # Resize the image to a smaller size for faster processing
    pil_image = Image.fromarray(image)
    pil_image = pil_image.resize((500, 500))
    image = np.array(pil_image)

    # Encode the face in the image
    face_encodings = face_recognition.face_encodings(image)
    if face_encodings:
        return face_encodings[0]
    return None

def load_and_process_image(image_file):
    # Load the image file
    image = Image.open(image_file)
    print("Image loaded successfully")

    # Convert the image to RGB if it is not already in that format
    if image.mode != 'RGB':
        image = image.convert('RGB')
        print("Image converted to RGB")

    # Resize the image to a smaller size for faster processing
    image = image.resize((500, 500))
    print("Image resized successfully")

    # Convert the image to a numpy array
    image = np.array(image)
    return image

class PhotoLibrarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PhotoLibrary
        fields = ['id', 'image', 'employee']

class AttendanceLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceLog
        fields = ['id', 'employee_id', 'selfie', 'location', 'att_date_time']

    def create(self, validated_data):
        selfie = validated_data.get('selfie')
        if selfie:
            # Load and process the selfie image file
            selfie_image = load_and_process_image(selfie)
            print("Selfie image loaded and processed successfully")

            # Save the loaded image for verification
            pil_image = Image.fromarray(selfie_image)
            pil_image.save("loaded_selfie.jpg")
            print("Selfie image saved for verification")

            # Encode the face in the selfie
            selfie_encoding = encode_face(selfie_image)
            if selfie_encoding is not None:
                print("Face encoding found in selfie")

                # Compare the selfie encoding with all employee photo encodings
                employees = Employee.objects.exclude(photo_encoding__isnull=True)
                for employee in employees:
                    employee_encoding = np.frombuffer(base64.b64decode(employee.photo_encoding), dtype=np.float64)
                    matches = face_recognition.compare_faces([employee_encoding], selfie_encoding)
                    if matches[0]:
                        print(f"Match found: {employee.name}")
                        validated_data['employee_id'] = employee
                        break
                else:
                    print("No match found")
            else:
                print("No face encodings found in selfie")
        else:
            print("No selfie provided")
        
        return super().create(validated_data)

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'client', 'attendanceRange', 'location',]
        
class EmployeeSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),  # Allow assigning project IDs
        many=True
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'employeeCode', 'email', 'phone',
            'designation', 'department', 'date_of_joining',  'user_id', 'projects', 'photo', 'photo_encoding'
        ]

    def to_representation(self, instance):
        """Modify output to include project titles instead of just IDs."""
        representation = super().to_representation(instance)
        representation['projects'] = [
            {"id": project.id, "title": project.title, 'range': project.attendanceRange, 'location': project.location} for project in instance.projects.all()
        ]
        return representation

    def create(self, validated_data):
        photo = validated_data.get('photo')
        if photo:
            # Load and process the photo image file
            photo_image = load_and_process_image(photo)
            print("Employee photo loaded and processed successfully")

            # Encode the face in the photo
            photo_encoding = encode_face(photo_image)
            if photo_encoding is not None:
                # Convert the encoding to a base64 string
                encoding_str = base64.b64encode(np.array(photo_encoding)).decode('utf-8')
                validated_data['photo_encoding'] = encoding_str
                print("Employee photo encoding saved")
            else:
                print("No face encodings found in employee photo")
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')
        if photo:
            # Load and process the photo image file
            photo_image = load_and_process_image(photo)
            print("Employee photo loaded and processed successfully")

            # Encode the face in the photo
            photo_encoding = encode_face(photo_image)
            if photo_encoding is not None:
                # Convert the encoding to a base64 string
                encoding_str = base64.b64encode(np.array(photo_encoding)).decode('utf-8')
                validated_data['photo_encoding'] = encoding_str
                print("Employee photo encoding saved")
            else:
                print("No face encodings found in employee photo")
        
        return super().update(instance, validated_data)