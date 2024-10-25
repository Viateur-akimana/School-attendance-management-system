from django.shortcuts import render, redirect
from .models import Student, Attendance
from .forms import MarkAttendanceForm

def attendance_view(request):
    attendance_list = Attendance.objects.all()
    students = Student.objects.all()
    return render(request, 'attendance/attendance.html', {'attendance_list': attendance_list, 'students': students})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def attendance_list(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'attendance/attendance_list.html', {'attendance_records': attendance_records})

def mark_attendance(request):
    if request.method == 'POST':
        form = MarkAttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance-view')
    else:
        form = MarkAttendanceForm()
    return render(request, 'attendance/mark_attendance.html', {'form': form})
