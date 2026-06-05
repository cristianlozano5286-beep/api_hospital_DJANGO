from django.db import models
from apps.base import BaseModel


class Pago(BaseModel):
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta_credito', 'Tarjeta de crédito'),
        ('tarjeta_debito', 'Tarjeta de débito'),
        ('transferencia', 'Transferencia bancaria'),
        ('pse', 'PSE'),
        ('eps', 'EPS / Seguro'),
        ('otro', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('exitoso', 'Exitoso'),
        ('pendiente', 'Pendiente'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]

    factura = models.ForeignKey(
        'facturas.Factura',
        on_delete=models.PROTECT,
        related_name='pagos',
        verbose_name='Factura',
    )
    fecha_pago = models.DateTimeField(verbose_name='Fecha y hora del pago')
    monto = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Monto pagado')
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, verbose_name='Método de pago')
    referencia_pago = models.CharField(
        max_length=100, blank=True,
        verbose_name='Referencia / Número de transacción',
    )
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='exitoso', verbose_name='Estado del pago')
    notas = models.TextField(blank=True, verbose_name='Notas')

    class Meta:
        db_table = '"hospital"."pagos"'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f'Pago {self.id} - Factura {self.factura.numero_factura} - ${self.monto}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._actualizar_estado_factura()

    def _actualizar_estado_factura(self):
        """Actualiza el estado de la factura según los pagos recibidos."""
        factura = self.factura
        total_pagado = sum(
            p.monto for p in factura.pagos.filter(estado='exitoso', activo=True)
        )
        if total_pagado >= factura.total:
            factura.estado = 'pagada'
        elif total_pagado > 0:
            factura.estado = 'parcial'
        factura.save(update_fields=['estado', 'fecha_modificacion'])
