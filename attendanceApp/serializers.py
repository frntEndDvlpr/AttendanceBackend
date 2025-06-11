from rest_framework import serializers
from .models import Employee, AttendanceLog, Project, WorkShift
from .import utils


class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = ['id', 'name', 'start_time', 'end_time', 'description']


class AttendanceLogSerializer(serializers.ModelSerializer):
    # shift = WorkShiftSerializer(read_only=True)

    class Meta:
        model = AttendanceLog
        fields = ['id', 'employee', 'selfie', 'location',
                  'att_date_time', 'date', 'time_in', 'time_out', 'total_hours', 'status', 'shift']

        read_only_fields = ['employee', 'date',
                            'time_in', 'time_out', 'status']

    def create(self, validated_data):
        selfie = validated_data.get('selfie')
        att_date_time = validated_data.get('att_date_time')
        validated_data['date'] = att_date_time.date()

        employee = self._match_employee_by_face(selfie)
        validated_data['employee'] = employee

        return self._handle_attendance_log(employee, att_date_time, selfie, validated_data)

    def _match_employee_by_face(self, selfie):
        known_employees = Employee.objects.exclude(photo_encoding__isnull=True)
        matched = utils.match_employee_by_selfie(selfie, known_employees)

        if not matched:
            raise serializers.ValidationError(
                "Face not recognized or not found.")

        return matched

    def _handle_attendance_log(self, employee, att_date_time, selfie, validated_data):
        log, created = AttendanceLog.objects.get_or_create(
            employee=employee,
            date=att_date_time.date(),
            defaults={
                'att_date_time': att_date_time,
                'selfie': selfie,
                'time_in': att_date_time.time()
            }
        )

        if not created:
            if log.time_out:
                raise serializers.ValidationError(
                    "Already punched out for today.")

            # Punch-out logic
            log.time_out = att_date_time.time()
            log.status = 'Present'
            log.selfie = selfie
            log.location = validated_data.get('location')
            log.total_hours = utils.compute_total_hours(
                log.time_in, log.time_out)
            log.save()
            return log

        # Punch-in logic
        log.location = validated_data.get('location')
        log.status = ''
        log.save()
        return log


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
