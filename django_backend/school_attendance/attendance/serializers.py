from rest_framework import serializers
from .models import Student,ClassRoom,Attendance,Notification,User
from django.contrib.auth import authenticate

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'
        
class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=ClassRoom
        fields='__all__'
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields='__all__'
class AttendReportSerializer(serializers.ModelSerializer):
    classroom_name=serializers.CharField(source='classroom.name')
    student_name=serializers.CharField(source='student.name')
    class Meta:
        model = Attendance
        fields = ['student_name', 'classroom_name', 'date', 'status']

 
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
