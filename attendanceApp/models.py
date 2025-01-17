from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    date_of_birth = models.DateField()
    address = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class PhotoLibrary(models.Model):
    image = models.ImageField(upload_to='images/')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.name
    
class AttendanceLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    status = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='images/')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.employee.name
        
class project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.name