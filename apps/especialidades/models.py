from django.db import models
from apps.base import BaseModel


class Especialidad(BaseModel):
    nombre = models.CharField(max_length=120, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    codigo = models.CharField(
        max_length=20, unique=True,
        verbose_name='Código',
        help_text='Código único de la especialidad (ej. CARD-01)',
    )

    class Meta:
        db_table = '"hospital"."especialidades"'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
