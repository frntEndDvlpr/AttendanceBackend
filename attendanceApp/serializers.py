from rest_framework import serializers
from .models import Employee, PhotoLibrary, AttendanceLog

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'employeeCode', 'email', 'phone', 'designation', 'department', 'date_of_joining']

class PhotoLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoLibrary
        fields = ['id', 'image', 'employee']

class AttendanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceLog
        fields = ['id', 'employee', 'date', 'time_in', 'time_out', 'status', 'photo', 'location']