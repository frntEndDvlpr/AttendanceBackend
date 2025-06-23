# filepath: /D:/Projects/AttendanceBackend/attendanceApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CorrectionRequestViewSet, EmployeeViewSet, AttendanceLogViewSet, ProjectViewSet, WorkShiftViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance-logs', AttendanceLogViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'work-shifts', WorkShiftViewSet)
router.register(r'correction-requests', CorrectionRequestViewSet, basename='correction-request')

urlpatterns = [
    path('', include(router.urls)),
]
