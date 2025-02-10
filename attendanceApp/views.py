from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Employee, PhotoLibrary, AttendanceLog, Project
from .serializers import EmployeeSerializer, PhotoLibrarySerializer, AttendanceLogSerializer, ProjectSerializer

# filepath: /D:/Projects/AttendanceBackend/attendanceApp/views.py
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False)
    def me(self, request):
        employee = Employee.objects.get(user_id=request.user.id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

class PhotoLibraryViewSet(viewsets.ModelViewSet):
    queryset = PhotoLibrary.objects.all()
    serializer_class = PhotoLibrarySerializer

class AttendanceLogViewSet(viewsets.ModelViewSet):
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer