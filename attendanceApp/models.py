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
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='employee')

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

    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    #date = models.DateField(blank=True, null=True)
    #time_in = models.TimeField(blank=True, null=True)
    #time_out = models.TimeField(blank=True, null=True)
    #status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, null=True)
    selfie = models.ImageField(upload_to='images/', blank=True, null=True)
    location = models.JSONField(blank=True, null=True)
    att_date_time = models.DateTimeField(blank=True, null=True)
    

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