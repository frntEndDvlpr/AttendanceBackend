from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee, PhotoLibrary, AttendanceLog
from .serializers import EmployeeSerializer, PhotoLibrarySerializer, AttendanceLogSerializer

# filepath: /D:/Projects/AttendanceBackend/attendanceApp/views.py
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class PhotoLibraryViewSet(viewsets.ModelViewSet):
    queryset = PhotoLibrary.objects.all()
    serializer_class = PhotoLibrarySerializer

class AttendanceLogViewSet(viewsets.ModelViewSet):
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer