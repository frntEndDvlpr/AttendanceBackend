# filepath: /D:/Projects/AttendanceBackend/attendanceApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PhotoLibraryViewSet, AttendanceLogViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'photo-libraries', PhotoLibraryViewSet)
router.register(r'attendance-logs', AttendanceLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]