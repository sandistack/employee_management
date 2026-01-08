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
        if self.parent and self.parent.level >= self.level:
            raise ValidationError(
                "Parent position must have lower level than this position."
            )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        if is_new and not self.group:
            self.group = Group.objects.create(name=f"Position: {self.name}")
        
        elif not is_new and self.group:
            old_position = Position.objects.get(pk=self.pk)
            if old_position.name != self.name:
                self.group.name = f"Position: {self.name}"
                self.group.save()
        
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete untuk handle soft delete.
        Cek apakah ini soft delete atau hard delete.
        """
        super().delete(*args, **kwargs)

    def hard_delete(self):
        """Hard delete: hapus Group juga"""
        if self.group:
            self.group.delete()
        
        super(AuditModel, self).delete()

    @property
    def permissions(self):
        """Get permissions dari group"""
        if self.group:
            return self.group.permissions.all()
        return []

    def __str__(self):
        return f"{self.code} - {self.name} (Level {self.level})"