from django.db import models
from apps.base import BaseModel


class Cita(BaseModel):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No asistió'),
    ]
    TIPO_CHOICES = [
        ('consulta', 'Consulta general'),
        ('control', 'Control'),
        ('urgencia', 'Urgencia'),
        ('procedimiento', 'Procedimiento'),
    ]

    paciente = models.ForeignKey(
        'pacientes.Paciente',
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Paciente',
    )
    medico = models.ForeignKey(
        'medicos.Medico',
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Médico',
    )
    fecha_hora = models.DateTimeField(verbose_name='Fecha y hora de la cita')
    duracion_minutos = models.PositiveSmallIntegerField(default=30, verbose_name='Duración (min)')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada', verbose_name='Estado')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='consulta', verbose_name='Tipo de cita')
    motivo_consulta = models.TextField(verbose_name='Motivo de consulta')
    diagnostico = models.TextField(blank=True, verbose_name='Diagnóstico')
    notas_medico = models.TextField(blank=True, verbose_name='Notas del médico')
    costo = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Costo')

    class Meta:
        db_table = '"hospital"."citas"'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f'Cita {self.id} - {self.paciente} con {self.medico} ({self.fecha_hora:%Y-%m-%d %H:%M})'
