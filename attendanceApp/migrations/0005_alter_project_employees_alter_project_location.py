# Generated by Django 5.1.5 on 2025-01-27 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceApp', '0004_rename_name_project_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='employees',
            field=models.ManyToManyField(blank=True, null=True, to='attendanceApp.employee'),
        ),
        migrations.AlterField(
            model_name='project',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
