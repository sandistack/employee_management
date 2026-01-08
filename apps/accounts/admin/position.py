from django.contrib import admin
from django.utils.html import format_html

from apps.accounts.models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Admin untuk Position dengan hierarchical display"""
    list_display = [
        'get_hierarchy', 'code', 'level', 'group', 'is_active'
    ]
    list_filter = ['level', 'is_active', 'parent']
    search_fields = ['name', 'code']
    ordering = ['level', 'code']
    
    fieldsets = [
        ('Basic Info', {
            'fields': ('name', 'code', 'level', 'group')
        }),
        ('Hierarchy', {
            'fields': ('parent',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    ]
    
    def get_hierarchy(self, obj):
        """Display hierarchy dengan indentation"""
        indent = '—' * obj.level
        if indent:
            indent += ' '
        return format_html(
            '<span style="color: #666;">{}</span>{}',
            indent,
            obj.name
        )
    get_hierarchy.short_description = 'Position'
    