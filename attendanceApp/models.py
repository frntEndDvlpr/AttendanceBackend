from django.conf import settings
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employeeCode = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    projects = models.ManyToManyField('Project', blank=True)
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class PhotoLibrary(models.Model):
    image = models.ImageField(upload_to='images/')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.name
    
class AttendanceLog(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('weekend', 'Weekend'),
        ('public_holiday', 'Public Holiday'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to='images/')
    location = models.JSONField()
    

    def __str__(self):
        return self.employee.name
        
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