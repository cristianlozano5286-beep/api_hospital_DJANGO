from django.db import models
from apps.base import BaseModel


class Medicamento(BaseModel):
    FORMA_FARMACEUTICA_CHOICES = [
        ('tableta', 'Tableta'),
        ('capsula', 'Cápsula'),
        ('jarabe', 'Jarabe'),
        ('inyectable', 'Inyectable'),
        ('crema', 'Crema'),
        ('gotas', 'Gotas'),
        ('supositorio', 'Supositorio'),
        ('parche', 'Parche'),
        ('otro', 'Otro'),
    ]

    nombre_generico = models.CharField(max_length=150, verbose_name='Nombre genérico')
    nombre_comercial = models.CharField(max_length=150, blank=True, verbose_name='Nombre comercial')
    codigo_registro = models.CharField(max_length=50, unique=True, verbose_name='Código de registro sanitario')
    laboratorio = models.CharField(max_length=120, blank=True, verbose_name='Laboratorio fabricante')
    forma_farmaceutica = models.CharField(
        max_length=20, choices=FORMA_FARMACEUTICA_CHOICES, verbose_name='Forma farmacéutica'
    )
    concentracion = models.CharField(max_length=80, verbose_name='Concentración', help_text='Ej: 500mg, 5mg/mL')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio unitario')
    requiere_receta = models.BooleanField(default=False, verbose_name='Requiere receta médica')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock disponible')

    class Meta:
        db_table = '"hospital"."medicamentos"'
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['nombre_generico']

    def __str__(self):
        return f'{self.nombre_generico} {self.concentracion} ({self.forma_farmaceutica})'
