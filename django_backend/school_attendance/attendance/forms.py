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
        fields = ['student', 'class_name', 'status', 'date']

    # Optionally, you can add any additional validation or field widgets
    # Example: limit students to those in the selected class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'class_name' in self.data:
            try:
                class_id = int(self.data.get('class_name'))
                self.fields['student'].queryset = Student.objects.filter(class_name_id=class_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['student'].queryset = self.instance.class_name.student_set.all()
class AttendanceFilterForm(forms.Form):
    class_name = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), required=False)
    date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    status = forms.ChoiceField(choices=[('', 'All'), ('Present', 'Present'), ('Absent', 'Absent')], required=False)