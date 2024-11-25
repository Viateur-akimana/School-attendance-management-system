from datetime import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Attendance, ClassRoom, Student, User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'class_name', 'roll_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'class_name': forms.Select(attrs={'class': 'form-select'}),
            'roll_number': forms.NumberInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }
    
class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name']
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'class_name', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_name'].queryset = ClassRoom.objects.all()
        self.fields['student'].queryset = Student.objects.all()