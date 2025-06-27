from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from attendanceApp.models import Employee

class UserCreateSerializer(BaseUserCreateSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'employee']

    def create(self, validated_data):
        employee = validated_data.pop('employee', None)

        # If using string (from FormData), coerce it
        if employee and isinstance(employee, str):
            try:
                employee = Employee.objects.get(pk=int(employee))
            except (ValueError, Employee.DoesNotExist):
                raise serializers.ValidationError({"employee": "Invalid employee ID"})

        user = super().create(validated_data)

        if employee:
            employee.user_id = user
            employee.save()

        return user


class UserSerializer(BaseUserSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    is_staff = serializers.BooleanField()

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'is_staff', 'employee']
