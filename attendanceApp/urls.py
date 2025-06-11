# filepath: /D:/Projects/AttendanceBackend/attendanceApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, AttendanceLogViewSet, ProjectViewSet, WorkShiftViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance-logs', AttendanceLogViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'work-shifts', WorkShiftViewSet)  # Added route for WorkShift

urlpatterns = [
    path('', include(router.urls)),
]
