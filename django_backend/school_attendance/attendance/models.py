from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        if not username:
            raise ValueError('Username is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    
class ClassRoom(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_student_count(self):
        return self.student_set.count()

    def __str__(self):
        return f"{self.name} ({self.get_student_count()} students)"
class Student(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)  # Link to ClassRoom model
    roll_number = models.IntegerField(unique=True)
    email = models.EmailField(unique=True,default="here@gmail.com")  # Email field added
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Roll No: {self.roll_number}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    class_name = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')],
        default='Absent',
    )

    def __str__(self):
        return f"{self.student.name} - {self.class_name.name} - {self.date} - {self.status}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == "Absent":
            create_absence_notification(self.student)
            

def create_absence_notification(student):
    """
    Creates a notification for absent students and sends an email.
    """
    # Define the title and message for the notification
    title = "Absence Alert"
    message = f"Dear {student.name}, you were marked as absent in class {student.class_name.name} on {timezone.now().date()}."

    # Create a Notification instance
    notification = Notification.objects.create(
        title=title,
        recipient_email=student.email,
        message=message
    )

    # Send the email
    send_absence_email(notification)

def send_absence_email(notification):
    """
    Sends an email notification for absent students.
    """
    send_mail(
        subject=notification.title,
        message=notification.message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[notification.recipient_email],
        fail_silently=False,
    )
    # Update notification as sent
    notification.is_sent = True
    notification.save()
    
class Notification(models.Model):
    title = models.CharField(max_length=100)  
    recipient_email = models.EmailField()    
    message = models.TextField()              
    created_at = models.DateTimeField(default=timezone.now)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} to {self.recipient_email}"