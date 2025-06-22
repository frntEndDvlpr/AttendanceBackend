from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from attendanceApp.models import Employee

class UserCreateSerializer(BaseUserCreateSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'employee']

class UserSerializer(BaseUserSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    is_staff = serializers.BooleanField(read_only=True)  # ✅ Safe and correct

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'is_staff', 'employee']
