from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer,ClassRoomSerializer,AttendanceSerializer,RegisterSerializer,LoginSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated




@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_students(request):
    students=Student.objects.all()
    serializer=StudentSerializer(students,many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_student(request):
    serializer= StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_id(request,student_id):
    try:
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Student.DoesNotExist :
        return Response({"error":"Student is not found"},status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_student(request,student_id):
    try:
        student= Student.objects.get(id=student_id)
    except Student.DoesNotExist :
        return Response({"error":"student not found"},status=status.HTTP_404_NOT_FOUND)
    student.delete()
    return Response(
        {"message": f"Student with ID {student_id} has been deleted."},
        status=status.HTTP_204_NO_CONTENT
    )   
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_classes(request):
    class_rooms=ClassRoom.objects.all()
    serializer=ClassRoomSerializer(class_rooms,many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_class(request):
        serializer=ClassRoomSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_class(request,class_id):
    try:
        classroom = ClassRoom.objects.get(id=class_id)
        serializer=ClassRoomSerializer(classroom)
        return Response(serializer.data)
    except ClassRoom.DoesNotExist :
        return Response({"error":"class room not found"},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_class(request,class_id):
    try:
        classroom = ClassRoom.objects.get(id=class_id)
    except ClassRoom.DoesNotExist :
        return Response({"error":"class room not found"},status=status.HTTP_404_NOT_FOUND)
    serializer=ClassRoomSerializer(classroom,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_class(request,class_id):
    try:
        classroom = ClassRoom.objects.get(id=class_id)
    except ClassRoom.DoesNotExist :
        return Response({"error":"class room not found"})
    classroom.delete()
    return Response({"message":f"Class room with ${class_id} has been deleted"},status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance(request):
    serializer = AttendanceSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance(request):
    date = request.query_params.get('date', None)
    student_id = request.query_params.get('student', None)
    classroom_id = request.query_params.get('classroom', None)

    attendance_records = Attendance.objects.all()

    if date:
        attendance_records = attendance_records.filter(date=date)
    if student_id:
        attendance_records = attendance_records.filter(student_id=student_id)
    if classroom_id:
        attendance_records = attendance_records.filter(classroom_id=classroom_id)

    serializer = AttendanceSerializer(attendance_records, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance_by_id(request, attendance_id):
    try:
        attendance = Attendance.objects.get(id=attendance_id)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_attendance(request, attendance_id):
    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_attendance(request, attendance_id):
    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found."}, status=status.HTTP_404_NOT_FOUND)

    attendance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
# Attendance Reports

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_summary(request):
    student_id = request.query_params.get('student_id', None)
    classroom_id = request.query_params.get('classroom_id', None)

    filters = {}
    if student_id:
        filters['student_id'] = student_id
    if classroom_id:
        filters['classroom_id'] = classroom_id

    attendance_records = Attendance.objects.filter(**filters)
    serializer = AttendanceSummarySerializer(attendance_records, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_attendance_report(request):

    today = timezone.now().date()
    attendance_records = Attendance.objects.filter(date=today)
    serializer = AttendanceSerializer(attendance_records, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_attendance_report(request):
    now = timezone.now()
    first_day_of_month = now.replace(day=1)

    attendance_records = Attendance.objects.filter(date__gte=first_day_of_month)
    serializer = AttendanceSerializer(attendance_records, many=True)

    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_and_send_notification(request):
    serializer = NotificationSerializer(data=request.data)
    
    if serializer.is_valid():
        notification = serializer.save()
        subject = "New Notification"
        message = notification.message
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = request.data.get('recipients', [])

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        
        notification.is_sent = True
        notification.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_attendance_alert(request):
    student_id = request.data.get('student_id')
    if not student_id:
        return Response({"error": "student_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    is_absent = check_if_absent(student_id) 

    if is_absent:
        message = f"Warning: Student with ID {student_id} has been marked absent."
        recipient_list = request.data.get('recipients', ['recipient@example.com'])  
        notification = Notification.objects.create(
            message=message,
            notification_type='email', 
            is_sent=False
        )

        send_mail(
            'Attendance Alert', 
            message, 
            settings.DEFAULT_FROM_EMAIL, 
            recipient_list,
            fail_silently=False,
        )
        
        notification.is_sent = True
        notification.save()
        
        return Response({"message": "Attendance alert sent."}, status=status.HTTP_201_CREATED)
    
    return Response({"message": "No alert sent. Student is present."}, status=status.HTTP_200_OK)

def check_if_absent(student_id):
    today = timezone.now().date()
    try:
        attendance_record = Attendance.objects.get(student_id=student_id, date=today)
        return not attendance_record.status
    except Attendance.DoesNotExist:
        return True 
    


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
    request,
    email=serializer.validated_data['email'],  # Change 'username' to 'email' if needed
    password=serializer.validated_data['password']
)


        
        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user(request):
    user = request.user
    if user.is_authenticated:
        data = {
            'username': user.username,
            'email': user.email,
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response({"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
