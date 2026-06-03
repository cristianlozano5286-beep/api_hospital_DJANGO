from django.db import models
from apps.base import BaseModel


class Paciente(BaseModel):
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]

    documento_identidad = models.CharField(max_length=20, unique=True, verbose_name='Documento de identidad')
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True, verbose_name='Género')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    correo_electronico = models.EmailField(blank=True, verbose_name='Correo electrónico')
    direccion = models.TextField(blank=True, verbose_name='Dirección')
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES, blank=True, verbose_name='Tipo de sangre')
    alergias = models.TextField(blank=True, verbose_name='Alergias conocidas')
    antecedentes_medicos = models.TextField(blank=True, verbose_name='Antecedentes médicos')
    contacto_emergencia_nombre = models.CharField(max_length=150, blank=True, verbose_name='Contacto de emergencia')
    contacto_emergencia_telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono emergencia')
    eps = models.CharField(max_length=100, blank=True, verbose_name='EPS / Aseguradora')

    class Meta:
        db_table = '"hospital"."pacientes"'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellidos', 'nombres']

    @property
    def nombre_completo(self) -> str:
        return f'{self.nombres} {self.apellidos}'

    def __str__(self):
        return f'{self.nombre_completo} ({self.documento_identidad})'
