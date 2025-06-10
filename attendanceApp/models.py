from django.conf import settings
from django.db import models
from .utils import encode_face_from_image_file


class Employee(models.Model):
    name = models.CharField(max_length=100)
    employeeCode = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    projects = models.ManyToManyField('Project', blank=True)
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='employee')
    photo = models.ImageField(
        upload_to='standardPhotos/', blank=True, null=True)
    photo_encoding = models.TextField(blank=True, null=True)
    work_shift = models.ForeignKey(
        'WorkShift', on_delete=models.SET_NULL, blank=True, null=True, related_name='employees')


def save(self, *args, **kwargs):
    if self.photo and not self.photo_encoding:
        self.photo.seek(0)  # Ensure file pointer is at start
        with self.photo.file as photo_file:
            encoding = encode_face_from_image_file(photo_file)
            if encoding:
                self.photo_encoding = encoding
    super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PhotoLibrary(models.Model):
    image = models.ImageField(upload_to='standardPhotos/')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.name


class AttendanceLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('weekend', 'Weekend'),
        ('public_holiday', 'Public Holiday'),
    ]

    employee_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, blank=True, null=True)
    selfie = models.ImageField(upload_to='selfies/', blank=True, null=True)
    location = models.CharField(blank=True, null=True)
    att_date_time = models.DateTimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    total_hours = models.FloatField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Present", blank=True, null=True)
    shift = models.ForeignKey(
        'WorkShift', on_delete=models.SET_NULL, blank=True, null=True, related_name='attendance_logs')

    def __str__(self):
        return self.employee_id.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    client = models.CharField(max_length=100, blank=True, null=True)
    location = models.JSONField(null=True, blank=True)
    attendanceRange = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title


class WorkShift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
