from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Employee, PhotoLibrary, AttendanceLog, Project, WorkShift
from .serializers import EmployeeSerializer, PhotoLibrarySerializer, AttendanceLogSerializer, ProjectSerializer, WorkShiftSerializer

class WorkShiftViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing WorkShift instances.
    """
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Employee instances.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False)
    def me(self, request):
        employee = Employee.objects.get(user_id=request.user.id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Custom logic for creating an Employee can be added here
        serializer.save()

    def perform_update(self, serializer):
        # Custom logic for updating an Employee can be added here
        serializer.save()

class PhotoLibraryViewSet(viewsets.ModelViewSet):
    queryset = PhotoLibrary.objects.all()
    serializer_class = PhotoLibrarySerializer

class AttendanceLogViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing AttendanceLog instances.
    """
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer

    def perform_create(self, serializer):
        # Custom logic for creating an AttendanceLog can be added here
        serializer.save()

    def perform_update(self, serializer):
        # Custom logic for updating an AttendanceLog can be added here
        serializer.save()

class ProjectViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Project instances.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
