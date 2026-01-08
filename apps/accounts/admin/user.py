from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'employee_id', 'username', 'get_full_name', 'email',
        'division', 'get_positions', 'status', 'is_active'
    ]
    
    list_display_links = ['employee_id', 'username']
    
    list_filter = [
        'is_active', 'is_staff', 'status',
        'type_of_employment', 'positions', 'division'
    ]
    search_fields = [
        'employee_id', 'username', 'email',
        'first_name', 'last_name'
    ]
    ordering = ['employee_id']
    
    filter_horizontal = ['positions']
 
    readonly_fields = ['face_encoding']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Employee Info', {
            'fields': (
                'employee_id', 'phone', 'division', 'positions',
                'hire_date', 'type_of_employment', 'status'
            )
        }),
        ('Face Recognition', {
            'fields': (
                'face_photo_front', 'face_photo_left',
                'face_photo_right', 'face_encoding'
            ),
            'classes': ('collapse',) 
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Employee Info', {
            'fields': (
                'employee_id', 'email', 'phone',
                'division', 'positions', 'hire_date'
            )
        }),
    )
    
    def get_positions(self, obj):
        """Display semua positions user"""
        if not obj.positions.exists():
            return '-'
        return ', '.join([pos.name for pos in obj.positions.all()])
    get_positions.short_description = 'Positions'