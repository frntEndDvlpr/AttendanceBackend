# filepath: /D:/Projects/AttendanceBackend/attendanceApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PhotoLibraryViewSet, AttendanceLogViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'photo-libraries', PhotoLibraryViewSet)
router.register(r'attendance-logs', AttendanceLogViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]