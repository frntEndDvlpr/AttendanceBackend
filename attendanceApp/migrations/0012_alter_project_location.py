# Generated by Django 5.1.5 on 2025-01-29 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceApp', '0011_alter_project_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='location',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
