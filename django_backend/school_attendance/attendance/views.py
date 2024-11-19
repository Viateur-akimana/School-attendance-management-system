from django.utils import timezone
from .models import Attendance, ClassRoom, Student
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import AttendanceFilterForm, AttendanceForm, ClassRoomForm, RegisterForm, LoginForm, StudentForm
from django.db.models import Q


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
        # Get data for the dashboard
        students = Student.objects.all()
        classrooms = ClassRoom.objects.all()
        today_attendance = Attendance.objects.filter(date=timezone.now().date())
        
        # Get attendance summary (for today, or per classroom)
        context = {
            'students': students,
            'classrooms': classrooms,
            'today_attendance': today_attendance,
        }

        return render(request, 'dashboard.html', context)
    else:
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
    selected_class_id = request.GET.get('class')  # Get selected class ID from query parameters
    classes = ClassRoom.objects.all()  # All classes
    students = Student.objects.filter(classroom_id=selected_class_id) if selected_class_id else Student.objects.none()
    current_date = timezone.now().date()

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance marked successfully.")
            return redirect('attendance_list')  # Redirect to the attendance list after marking
        else:
            messages.error(request, "Error marking attendance. Please check the form.")
    else:
        form = AttendanceForm()

    return render(request, 'mark_attendance.html', {
        'form': form,
        'classes': classes,
        'students': students,
        'selected_class_id': selected_class_id,
        'current_date': current_date,
    })

# View to list attendance records (optional)
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance_list.html', {'attendances': attendances})


def attendance_report(request):
    form = AttendanceFilterForm(request.GET)
    attendance_records = Attendance.objects.all()

    if form.is_valid():
        if form.cleaned_data['class_name']:
            attendance_records = attendance_records.filter(class_name=form.cleaned_data['class_name'])
        if form.cleaned_data['date']:
            attendance_records = attendance_records.filter(date=form.cleaned_data['date'])
        if form.cleaned_data['status']:
            attendance_records = attendance_records.filter(status=form.cleaned_data['status'])

    return render(request, 'attendance/attendance_report.html', {
        'form': form,
        'attendance_records': attendance_records,
    })