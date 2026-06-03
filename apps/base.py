"""
Modelo base con campos comunes para todas las tablas.
Todos los modelos del proyecto deben heredar de BaseModel.
"""
from django.db import models


class BaseModel(models.Model):
    """
    Modelo abstracto base.
    Proporciona los campos auditables requeridos:
      - activo
      - fecha_creacion
      - fecha_modificacion
    """
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el registro está activo en el sistema.',
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación',
    )

    class Meta:
        abstract = True

    def desactivar(self):
        """Soft-delete: desactiva el registro sin eliminarlo."""
        self.activo = False
        self.save(update_fields=['activo', 'fecha_modificacion'])

    def activar(self):
        self.activo = True
        self.save(update_fields=['activo', 'fecha_modificacion'])
