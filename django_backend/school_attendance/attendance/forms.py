# attendance/forms.py
from django import forms
from .models import Attendance

class MarkAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'status']