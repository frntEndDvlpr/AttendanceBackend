from djoser.serializers import UserSerializer as BaseUserSerializer

from attendanceApp.serializers import EmployeeSerializer

class UserSerializer(BaseUserSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta (BaseUserSerializer.Meta):
        fields = ['id', 'username','email','employee']