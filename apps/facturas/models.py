from django.db import models
from apps.base import BaseModel


class Factura(BaseModel):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('parcial', 'Parcialmente pagada'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada'),
    ]

    paciente = models.ForeignKey(
        'pacientes.Paciente',
        on_delete=models.PROTECT,
        related_name='facturas',
        verbose_name='Paciente',
    )
    numero_factura = models.CharField(max_length=30, unique=True, verbose_name='Número de factura')
    fecha_emision = models.DateField(verbose_name='Fecha de emisión')
    fecha_vencimiento = models.DateField(verbose_name='Fecha de vencimiento')
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='Subtotal')
    descuento = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='Descuento')
    impuesto = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='Impuesto (IVA)')
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='Total')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente', verbose_name='Estado')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    cita = models.ForeignKey(
        'citas.Cita',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='facturas',
        verbose_name='Cita asociada',
    )

    class Meta:
        db_table = '"hospital"."facturas"'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']

    def __str__(self):
        return f'Factura {self.numero_factura} - {self.paciente} ({self.estado})'

    def calcular_total(self):
        self.total = self.subtotal - self.descuento + self.impuesto
        self.save(update_fields=['total', 'fecha_modificacion'])
