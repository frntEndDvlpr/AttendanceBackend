from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employeeCode = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)

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
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.employee.name
        
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    employees = models.ManyToManyField(Employee)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name