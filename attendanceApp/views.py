from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from .models import CorrectionRequest, Employee, AttendanceLog, Project, WorkShift
from .serializers import CorrectionRequestSerializer, EmployeeSerializer, AttendanceLogSerializer, ProjectSerializer, WorkShiftSerializer, CorrectionReviewSerializer
from .utils import compute_total_hours

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


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.employee == request.user or request.user.is_staff

class CorrectionRequestViewSet(viewsets.ModelViewSet):
    queryset = CorrectionRequest.objects.all()
    serializer_class = CorrectionRequestSerializer
    permission_classes = [IsEmployeeOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        date = serializer.validated_data.get('date')

        # Try to find an Employee linked to this user
        try:
            employee = Employee.objects.get(user_id=user)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Employee profile not found for the current user.")

        # Attempt to find the related AttendanceLog for that date
        try:
            attendance_log = AttendanceLog.objects.get(employee=employee, date=date)
        except AttendanceLog.DoesNotExist:
            attendance_log = None  # it's OK if there's no log yet

        # Save the correction request with the employee and matched log
        serializer.save(employee=user, attendance_log=attendance_log)

    @action(
    detail=True,
    methods=['get', 'post'],
    permission_classes=[permissions.IsAdminUser],
    serializer_class=CorrectionReviewSerializer
    )
    def review(self, request, pk=None):
        correction = self.get_object()

        if request.method == 'GET':
            serializer = CorrectionReviewSerializer()
            return Response(serializer.data)

        serializer = CorrectionReviewSerializer(data=request.data)
        if serializer.is_valid():
            decision = serializer.validated_data['decision']
            correction.status = decision
            correction.reviewed_by = request.user
            correction.reviewed_at = timezone.now()
            correction.save()

            # ✅ Auto-update AttendanceLog if approved
            if decision == 'APPROVED' and correction.attendance_log:
                att_log = correction.attendance_log

                # Apply the corrected time
                if correction.punch_type == 'IN':
                    att_log.time_in = correction.corrected_time
                elif correction.punch_type == 'OUT':
                    att_log.time_out = correction.corrected_time

                # If both times are available, update total_hours and status
                if att_log.time_in and att_log.time_out:
                    att_log.total_hours = compute_total_hours(att_log.time_in, att_log.time_out)
                    att_log.status = 'present'  # or 'Present', depending on your convention

                att_log.save()

            return Response({'status': correction.status})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
