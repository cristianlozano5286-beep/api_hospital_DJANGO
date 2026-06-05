from django.db import models
from apps.base import BaseModel


class Tratamiento(BaseModel):
    VIA_ADMINISTRACION_CHOICES = [
        ('oral', 'Oral'),
        ('intravenosa', 'Intravenosa'),
        ('intramuscular', 'Intramuscular'),
        ('topica', 'Tópica'),
        ('subcutanea', 'Subcutánea'),
        ('inhalada', 'Inhalada'),
        ('otra', 'Otra'),
    ]

    cita = models.ForeignKey(
        'citas.Cita',
        on_delete=models.PROTECT,
        related_name='tratamientos',
        verbose_name='Cita',
    )
    medicamento = models.ForeignKey(
        'medicamentos.Medicamento',
        on_delete=models.PROTECT,
        related_name='tratamientos',
        verbose_name='Medicamento',
    )
    dosis = models.CharField(max_length=100, verbose_name='Dosis', help_text='Ej: 1 tableta')
    frecuencia = models.CharField(max_length=100, verbose_name='Frecuencia', help_text='Ej: Cada 8 horas')
    duracion_dias = models.PositiveSmallIntegerField(verbose_name='Duración (días)')
    via_administracion = models.CharField(
        max_length=20, choices=VIA_ADMINISTRACION_CHOICES, default='oral', verbose_name='Vía de administración'
    )
    indicaciones = models.TextField(blank=True, verbose_name='Indicaciones adicionales')
    cantidad_dispensada = models.PositiveSmallIntegerField(default=0, verbose_name='Cantidad dispensada')
    costo_tratamiento = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Costo del tratamiento'
    )

    class Meta:
        db_table = '"hospital"."tratamientos"'
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Tratamiento {self.id}: {self.medicamento} - Cita {self.cita_id}'
