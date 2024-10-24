from rest_framework import generics
from .models import Attendance
from .serializers import AttendanceSerializer, MarkAttendanceSerializer

class AttendanceListView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class MarkAttendanceView(generics.CreateAPIView):
    serializer_class = MarkAttendanceSerializer
