from rest_framework import serializers
from .models import Employee, PhotoLibrary, AttendanceLog, Project, WorkShift
from .import utils


class PhotoLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoLibrary
        fields = ['id', 'image', 'employee']


class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = ['id', 'name', 'start_time', 'end_time', 'description']


class AttendanceLogSerializer(serializers.ModelSerializer):
    # shift = WorkShiftSerializer(read_only=True)

    class Meta:
        model = AttendanceLog
        fields = ['id', 'employee_id', 'selfie', 'location',
                  'att_date_time', 'date', 'time_in', 'time_out', 'total_hours', 'status', 'shift']

        read_only_fields = ['employee_id', 'date',
                            'time_in', 'time_out', 'status']

    def create(self, validated_data):
        selfie = validated_data.get('selfie')
        att_date_time = validated_data.get('att_date_time')

        validated_data['date'] = att_date_time.date()

        # Match face in the selfie to employee
        known_employees = Employee.objects.exclude(photo_encoding__isnull=True)
        matched_employee = utils.match_employee_by_selfie(
            selfie, known_employees)

        if not matched_employee:
            raise serializers.ValidationError(
                "Face not recognized or not found.")

        validated_data['employee_id'] = matched_employee

        # Check if there's already an entry for today
        attendance_log, created = AttendanceLog.objects.get_or_create(
            employee_id=matched_employee,
            date=att_date_time.date(),
            defaults={
                'att_date_time': att_date_time,
                'selfie': selfie,
                'time_in': att_date_time.time()
            }
        )

        if not created:
            # This is a punch-out
            if attendance_log.time_out:
                raise serializers.ValidationError(
                    "Already punched out for today.")

            attendance_log.location = validated_data.get('location', None)
            attendance_log.time_out = att_date_time.time()
            attendance_log.status = 'Present'
            attendance_log.selfie = selfie  # Optional: save punch-out selfie
            attendance_log.total_hours = utils.compute_total_hours(
                attendance_log.time_in,
                attendance_log.time_out
            )
            attendance_log.save()
            return attendance_log

        # This is a punch-in
        attendance_log.location = validated_data.get('location', None)
        attendance_log.status = ''
        attendance_log.save()
        return attendance_log


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date',
                  'end_date', 'client', 'attendanceRange', 'location',]


class EmployeeSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), many=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'employeeCode', 'email', 'phone',
            'designation', 'department', 'date_of_joining', 'user_id',
            'projects', 'photo', 'photo_encoding', 'work_shift'
        ]

    def to_representation(self, instance):
        """
        Convert the instance to a dictionary representation,
        including project details.
        """
        data = super().to_representation(instance)
        data['projects'] = [
            {"id": project.id, "title": project.title,
             "range": project.attendanceRange, "location": project.location}
            for project in instance.projects.all()
        ]
        return data

    def create(self, validated_data):
        photo = validated_data.get('photo')
        if photo:
            encoding = utils.encode_face_from_image_file(photo)
            if encoding:
                validated_data['photo_encoding'] = encoding
        return super().create(validated_data)

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')
        if photo:
            encoding = utils.encode_face_from_image_file(photo)
            if encoding:
                validated_data['photo_encoding'] = encoding
        return super().update(instance, validated_data)
