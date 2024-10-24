# attendance/urls.py
from django.urls import path
from .views import AttendanceListView, MarkAttendanceView

urlpatterns = [
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/mark/', MarkAttendanceView.as_view(), name='mark-attendance'),
]
