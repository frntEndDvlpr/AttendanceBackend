# Generated by Django 5.1.5 on 2025-01-26 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceApp', '0002_rename_code_employee_employeecode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]