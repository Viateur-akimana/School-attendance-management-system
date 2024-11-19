from django.urls import path
from .views import attendance_list, attendance_report, create_class, dashboard,create_student, delete_class, get_class, list_classes, list_students, mark_attendance, update_class,update_student,delete_student,register_user,login_user,logout_user

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('students/', list_students, name='list_students'),
    path('students/create/', create_student, name='create_student'),
    path('students/update/<int:student_id>/', update_student, name='update_student'),
    path('students/delete/<int:student_id>/', delete_student, name='delete_student'), 
    path('classes/', list_classes, name='list_classes'),
    path('classes/create/', create_class, name='create_class'),
    path('classes/<int:pk>/update/', update_class, name='update_class'),
     path('class/<int:class_id>/delete/', delete_class, name='delete_class'),
    path('class/<int:class_id>/', get_class, name='get_class'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('attendance_list/', attendance_list, name='attendance_list'),
    path('attendance_report',attendance_report,name='attendance_report'),
    path('logout',login_user,name="logout_user")

]
