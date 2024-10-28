from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Student, ClassRoom, Attendance, Notification

class CustomUserAdmin(BaseUserAdmin):
    # Define fields to display in the list view
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')

    # Define how fields are grouped in the user detail page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Define the fields required when adding a new user through the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    # Search and order users by email and username
    search_fields = ('email', 'username')
    ordering = ('email',)

# Register the custom User model with the updated UserAdmin class
admin.site.register(User, CustomUserAdmin)


# Registering other models
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'roll_number', 'created_at', 'updated_at')
    search_fields = ('name', 'class_name')
    ordering = ('roll_number',)


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at', 'updated_at')
    search_fields = ('name', 'subject')
    ordering = ('name',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'date', 'status', 'created_at')
    search_fields = ('student__name', 'classroom__name')
    list_filter = ('status', 'date')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_sent', 'created_at')
    search_fields = ('message',)
    list_filter = ('is_sent',)
