from django.urls import path
from .views import student_list, attendance_list, mark_attendance, attendance_view

urlpatterns = [
    path('', attendance_view, name='attendance-view'),  # Main attendance dashboard
    path('students/', student_list, name='student-list'),  # View all students
    path('attendance/', attendance_list, name='attendance-list'),  # List of attendance records
    path('attendance/mark/', mark_attendance, name='mark-attendance'),  # Mark attendance
]
