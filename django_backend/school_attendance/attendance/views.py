from django.utils import timezone
from .models import Attendance, ClassRoom, Student
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import AttendanceForm, ClassRoomForm, RegisterForm, LoginForm, StudentForm, Attendance
from django.db.models import Q
from django.utils.dateparse import parse_date
import json
from datetime import datetime, timedelta
from .models import ClassRoom, Attendance  


# Register view
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login_user/')

def dashboard(request):
    if request.user.is_authenticated:
        classes = ClassRoom.objects.all()
        attendance_data = {}
        today = timezone.now().date()

        for class_obj in classes:
            # Get today's attendance
            today_attendance = Attendance.objects.filter(
                class_name=class_obj,
                date=today
            )

            # Calculate weekly attendance (last 7 days)
            weekly_absence = []
            for i in range(6, -1, -1):  # Last 7 days
                date = today - timedelta(days=i)
                absent_count = Attendance.objects.filter(
                    class_name=class_obj,
                    date=date,
                    status='Absent'
                ).count()
                weekly_absence.append(absent_count)

            # Store data for this class
            attendance_data[str(class_obj.id)] = {
                'present': today_attendance.filter(status='Present').count(),
                'absent': today_attendance.filter(status='Absent').count(),
                'late': today_attendance.filter(status='Late').count(),
                'weekly_absence': weekly_absence
            }

        context = {
            'classes': classes,
            'attendance_data': json.dumps(attendance_data),
            'user': request.user
        }
        return render(request, 'dashboard.html', context)
    return redirect('login')

# List all students
def list_students(request):
    # Get the search query from the GET request (if it exists)
    query = request.GET.get('search', '')  # Defaults to an empty string if no search query is provided
    
    # Filter students based on the search query
    if query:
        students = Student.objects.filter(
            Q(roll_number__icontains=query) | Q(name__icontains=query)
        )
    else:
        students = Student.objects.all()  # If no search query, show all students
    
    # Pass the students and the search query to the template
    context = {
        'students': students,
        'query': query,
    }
    return render(request, 'students/students.html', context)

# Create a new student

def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        form = StudentForm()
    
    return render(request, 'students/create_student.html', {'form': form})

# Update an existing student
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect('list_students')
        else:
            messages.error(request, "Error updating student.")
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/update_student.html', {'form': form, 'student': student})

# Delete a student
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect('list_students')
        
def list_classes(request):
    classes = ClassRoom.objects.all()
    return render(request, 'class/classes.html', {'classes': classes})


def create_class(request):
    if request.method == 'POST':
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_classes')
    else:
        form = ClassRoomForm()
    return render(request, 'class/create_class.html', {'form': form})

def update_class(request, pk):
    classroom = ClassRoom.objects.get(pk=pk)
    if request.method == 'POST':
        form = ClassRoomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('list_classes')
    else:
        form = ClassRoomForm(instance=classroom)
    return render(request, 'class/create_class.html', {'form': form})
def delete_class(request, class_id):
    classroom = get_object_or_404(ClassRoom, id=class_id)
    classroom.delete()
    messages.success(request, "Class deleted successfully.")
    return redirect('list_classes')
def get_class(request, class_id):
    classroom = get_object_or_404(ClassRoom, id=class_id)
    return render(request, 'class/class_detail.html', {'classroom': classroom})

def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():

            form.save()
            messages.success(request, "Attendance has been recorded.")
    
            return redirect('attendance_list')
    else:
        form = AttendanceForm()

    return render(request, 'attendance/mark_attendance.html', {'form': form})


def attendance_list(request):
    # Fetch all attendance records
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

def attendance_report(request):
    filter_class = request.GET.get('class', '')
    filter_date = request.GET.get('date', '')
    filter_status = request.GET.get('status', '')

    # Filtering logic
    attendance_records = Attendance.objects.all()

    if filter_class:
        attendance_records = attendance_records.filter(class_name_id=filter_class)
    
    if filter_date:
        filter_date = parse_date(filter_date)
        attendance_records = attendance_records.filter(date=filter_date)
    
    if filter_status:
        attendance_records = attendance_records.filter(status=filter_status)

    class_list = ClassRoom.objects.all()

    return render(request, 'attendance/attendance_report.html', {
        'attendance_records': attendance_records,
        'class_list': class_list,
        'filter_class': filter_class,
        'filter_date': filter_date,
        'filter_status': filter_status,
    }) 



def dashboard_view(request):
    classes = ClassRoom.objects.all()
    attendance_data = {}

    for cls in classes:
        # Calculate today's attendance breakdown
        today_attendance = Attendance.objects.filter(class_name=cls, date=datetime.date.today())
        present_count = today_attendance.filter(status="Present").count()
        absent_count = today_attendance.filter(status="Absent").count()
        late_count = today_attendance.filter(status="Late").count()
        
        # Weekly absence trend (Mon-Sun)
        weekly_absence = [
            Attendance.objects.filter(class_name=cls, status="Absent", date__week_day=i).count()
            for i in range(2, 9)  # Django weekday 2=Monday to 8=Sunday
        ]

        attendance_data[cls.id] = {
            'present': present_count,
            'absent': absent_count,
            'late': late_count,
            'weekly_absence': weekly_absence,
        }

    return render(request, 'dashboard.html', {
        'classes': classes,
        'attendance_data': attendance_data,
    })