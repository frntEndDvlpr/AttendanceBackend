# Generated by Django 5.1.5 on 2025-01-31 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceApp', '0017_project_range'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='range',
            new_name='attendanceRange',
        ),
    ]
