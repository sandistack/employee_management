# core/models/permissions.py
from django.db import models


class CorePermission(models.Model):
    """
    Permission anchor model.
    Used ONLY for custom permissions.
    """

    class Meta:
        verbose_name = "Core Permission"
        verbose_name_plural = "Core Permissions"
        default_permissions = ()
        permissions = [
            # DASHBOARD
            ("view_company_dashboard", "Can view company-wide dashboard"),
            ("view_division_dashboard", "Can view division dashboard"),
            ("view_own_dashboard", "Can view own dashboard"),
            ("export_dashboard_data", "Can export dashboard data"),

            # ATTENDANCE
            ("approve_attendance", "Can approve attendance"),
            ("view_all_attendance_report", "Can view all attendance reports"),

            # LEAVE
            ("approve_all_leaves", "Can approve all leaves"),
            ("reject_leave", "Can reject leave"),
            ("cancel_approved_leave", "Can cancel approved leave"),

            # REPORT
            ("export_attendance_report", "Can export attendance report"),
            ("export_leave_report", "Can export leave report"),
            ("export_payroll_report", "Can export payroll report"),
            ("view_analytics", "Can view analytics dashboard"),
        ]
