# Generated by Django 5.1.5 on 2025-02-27 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceApp', '0008_employee_photo_encoding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo_encoding',
            field=models.TextField(),
        ),
    ]
