from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

from attendanceApp.models import Employee


class UserCreateSerializer(BaseUserCreateSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)

    class Meta (BaseUserCreateSerializer.Meta):
        fields = ['id', 'username','email', 'password', 'employee']