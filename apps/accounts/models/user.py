from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.utils import now
from apps.core.validators import validate_email_domain, validate_phone_number


class User(AbstractUser):
    """
    Custom User Model.

    Responsibility:
    - Store employee data
    - Authentication
    - Authorization via Group & Permission (Django native)

    IMPORTANT:
    - No hardcoded roles
    - No role logic here
    """

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    # ================= EMPLOYEE INFO =================

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text='ID unik karyawan, contoh: EMP0001'
    )

    email = models.EmailField(
        unique=True,
        validators=[validate_email_domain],
        help_text='Alamat email karyawan (harus domain perusahaan)'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[validate_phone_number],
        help_text='Nomor telepon karyawan (08xxx atau 62xxx)'
    )

    division = models.ForeignKey(
        'accounts.Division',
        on_delete=models.PROTECT,
        related_name='employees',
        null=True,
        blank=True,
        help_text='Divisi/Departemen organisasi (opsional)'
    )

    position = models.ForeignKey(
        'accounts.Position',
        on_delete=models.PROTECT,
        related_name='employees',
        null=True,
        blank=True,
        help_text='Jabatan/posisi pekerjaan (opsional)'
    )

    hire_date = models.DateField(
        null=True,
        blank=True,
        help_text='Tanggal mulai bekerja (opsional)'
    )

    type_of_employment = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text='Jenis kepegawaian (full time, kontrak, magang, dll)'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_index=True,
        help_text='Status kepegawaian (aktif, cuti, resign, dll)'
    )

    # ================= FACE RECOGNITION =================

    face_photo_front = models.ImageField(
        upload_to='faces/front/%Y/%m/',
        null=True,
        blank=True,
        help_text='Foto wajah tampak depan (opsional)'
    )
    face_photo_left = models.ImageField(
        upload_to='faces/left/%Y/%m/',
        null=True,
        blank=True,
        help_text='Foto wajah tampak kiri (opsional)'
    )
    face_photo_right = models.ImageField(
        upload_to='faces/right/%Y/%m/',
        null=True,
        blank=True,
        help_text='Foto wajah tampak kanan (opsional)'
    )

    face_encoding = models.JSONField(
        null=True,
        blank=True,
        editable=False,
        help_text='Data encoding wajah untuk face recognition (otomatis)'
    )

    # ================= AUDIT (SOFT DELETE) =================

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Waktu data dihapus (soft delete)'
    )
    deleted_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_users',
        help_text='User yang menghapus data ini (soft delete)'
    )

    class Meta:
        db_table = 'users'
        ordering = ['employee_id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['division', 'is_active']),
        ]

    def __str__(self):
        return f"{self.employee_id} - {self.get_full_name() or self.username}"

    # ================= SOFT DELETE =================

    def soft_delete(self, user=None):
        self.is_active = False
        self.deleted_at = now()
        if user:
            self.deleted_by = user
        self.save(update_fields=['is_active', 'deleted_at', 'deleted_by'])

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['is_active', 'deleted_at', 'deleted_by'])

    # ================= HELPERS (NON ROLE) =================

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    @property
    def is_employed(self):
        return self.status in ['active', 'on_leave']

    @property
    def is_terminated(self):
        return self.status == 'terminated'

    def get_division_path(self):
        return self.division.full_path if self.division else "-"

    def get_role_display(self):
        """Display role berdasarkan position atau groups"""
        if self.position:
            return self.position.name
        groups = self.groups.all()
        if groups:
            return ", ".join([g.name for g in groups])
        return "-"
