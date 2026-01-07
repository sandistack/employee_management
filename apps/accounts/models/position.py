# accounts/models/position.py
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models.base import AuditModel


class Position(AuditModel):
    """
    Hirarki Jabatan (authority level), BUKAN struktur organisasi.

    Contoh:
        Level 1 → Staff
        Level 2 → Supervisor
        Level 3 → Manager
        Level 4 → HR
        Level 5 → CEO
    """

    name = models.CharField(
        max_length=100,
        help_text="Nama jabatan (Staff, Supervisor, Manager, HR, CEO)"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Kode jabatan (STF, SPV, MGR, HR, CEO)"
    )

    level = models.PositiveSmallIntegerField(
        db_index=True,
        help_text="Semakin besar, semakin tinggi jabatan"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="subordinates",
        help_text="Atasan langsung (opsional, untuk navigasi hirarki)"
    )

    group = models.OneToOneField(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="position",
        help_text="Django Groups (hak akses) untuk jabatan ini"
    )

    class Meta:
        db_table = "positions"
        ordering = ["level"]
        unique_together = [["level", "code"]]
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def clean(self):
        """
        Validasi konsistensi hirarki.
        """
        if self.parent and self.parent.level >= self.level:
            raise ValidationError(
                "Parent position must have lower level than this position."
            )

    def sync_user_groups(self):
        """
        Sinkronisasi Django Groups untuk semua user dengan jabatan ini.
        """
        if not self.group:
            return
        
        users = self.employees.all()
        for user in users:
            user.groups.clear()
            user.groups.add(self.group)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.sync_user_groups()

    def delete(self, *args, **kwargs):
        """
        Hapus relasi Group saat menghapus jabatan.
        """
        if self.group:
            self.group.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name} (Level {self.level})"
