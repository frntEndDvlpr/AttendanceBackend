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
    projects=ProjectSerializer(many=True)
    class Meta:
        model = Employee
        fields = ['id', 'name', 'employeeCode', 'email', 'phone', 'designation', 'department', 'projects', 'date_of_joining']