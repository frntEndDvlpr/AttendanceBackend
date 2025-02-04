from rest_framework import serializers
from .models import Employee, PhotoLibrary, AttendanceLog, Project


class PhotoLibrarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PhotoLibrary
        fields = ['id', 'image', 'employee']

class AttendanceLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceLog
        fields = ['id', 'employee', 'date', 'time_in', 'time_out', 'status', 'photo', 'location']
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
            'id', 'name', 'employeeCode', 'email', 'phone',  'user',
            'designation', 'department', 'projects', 'date_of_joining'
        ]

    def to_representation(self, instance):
        """Modify output to include project titles instead of just IDs."""
        representation = super().to_representation(instance)
        representation['projects'] = [
            {"id": project.id, "title": project.title} for project in instance.projects.all()
        ]
        return representation

