# Generated by Django 5.2.3 on 2025-06-27 16:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceApp', '0004_correctionrequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='correctionrequest',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='correctionrequest',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_corrections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employeeCode',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
