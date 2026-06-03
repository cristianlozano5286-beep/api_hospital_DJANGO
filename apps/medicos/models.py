from django.db import models
from apps.base import BaseModel


class Medico(BaseModel):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    especialidad = models.ForeignKey(
        'especialidades.Especialidad',
        on_delete=models.PROTECT,
        related_name='medicos',
        verbose_name='Especialidad',
    )
    numero_registro = models.CharField(
        max_length=30, unique=True,
        verbose_name='Número de registro médico',
    )
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    documento_identidad = models.CharField(max_length=20, unique=True, verbose_name='Documento de identidad')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    correo_electronico = models.EmailField(unique=True, verbose_name='Correo electrónico')
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True, verbose_name='Género')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    anos_experiencia = models.PositiveSmallIntegerField(default=0, verbose_name='Años de experiencia')

    class Meta:
        db_table = '"hospital"."medicos"'
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering = ['apellidos', 'nombres']

    @property
    def nombre_completo(self) -> str:
        return f'{self.nombres} {self.apellidos}'

    def __str__(self):
        return f'Dr(a). {self.nombre_completo} ({self.especialidad})'
