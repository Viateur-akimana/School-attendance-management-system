from django.urls import path
from .views import get_students,create_student,get_student_id,update_student,delete_student,list_classes,get_single_class,update_class,delete_class,create_class,get_attendance,get_attendance_by_id,update_attendance,mark_attendance,delete_attendance,create_and_send_notification,list_notifications,send_attendance_alert,register_user,login_user,logout_user,get_user

urlpatterns = [
    path('students/', get_students, name='get_students'), 
    path('students/create',create_student,name='create_student'),
    path('students/<int:student_id>',get_student_id,name="get_student_id"),
    path('students/update/<int:student_id>',update_student,name='update_student'),
    path('students/delete/<int:student_id>',delete_student,name="delete_student"),
    path('class/', list_classes, name='list_classes'), 
    path('class/create',create_class,name='create_class'),
    path('class/<int:class_id>',get_single_class,name="get_single_class"),
    path('class/update/<int:class_id>',update_class,name='update_class'),
    path('class/delete/<int:class_id>',delete_class,name="delete_class"),
    path('attendance/', get_attendance, name='get_attendance'), 
    path('attendance/create',mark_attendance,name='mark_attendance'),
    path('attendance/<int:attendance_id>',get_attendance_by_id,name="get_attendance_by_id"),
    path('attendance/update/<int:attendance_id>',update_attendance,name='update_attendance'),
    path('attendance/delete/<int:attendance_id>',update_attendance,name="update_attendance"),
    path('notifications/', create_and_send_notification, name='create_and_send_notification'),
    path('notifications/', list_notifications, name='list_notifications'), 
    path('notifications/attendance-alert/', send_attendance_alert, name='send_attendance_alert'),
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/user/', get_user, name='user-details'),

]
