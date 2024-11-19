from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import Attendance, User, Student, ClassRoom, Notification
from .forms import RegisterForm, StudentForm

class CustomUserAdmin(BaseUserAdmin):
    # Use custom registration form
    add_form = RegisterForm
    
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('name', 'class_name', 'roll_number', 'email', 'created_at', 'updated_at')
    list_filter = ('class_name', 'created_at')
    search_fields = ('name', 'email', 'roll_number')
    ordering = ('roll_number',)
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Student Information'), {
            'fields': ('name', 'class_name', 'roll_number', 'email')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    def student_count(self, obj):
        return obj.get_student_count()
    student_count.short_description = _('Number of Students')
    
    fieldsets = (
        (_('Class Information'), {
            'fields': ('name',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message_preview', 'recipients_count', 'is_sent', 'created_at')
    list_filter = ('is_sent', 'created_at')
    search_fields = ('message', 'recipients')
    readonly_fields = ('created_at',)
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = _('Message')
    
    def recipients_count(self, obj):
        return len(obj.recipients)
    recipients_count.short_description = _('Number of Recipients')
    
    fieldsets = (
        (_('Notification Details'), {
            'fields': ('message', 'recipients', 'is_sent')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_name', 'date', 'status')
    list_filter = ('class_name', 'status', 'date')
    search_fields = ('student__name', 'class_name__name', 'date')
    ordering = ('date', 'student__roll_number')
    
    fieldsets = (
        (_('Attendance Details'), {
            'fields': ('student', 'class_name', 'date', 'status')
        }),
    )


# Register the custom User model
admin.site.register(User, CustomUserAdmin)