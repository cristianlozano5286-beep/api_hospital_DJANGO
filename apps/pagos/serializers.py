from rest_framework import serializers
from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    numero_factura = serializers.ReadOnlyField(source='factura.numero_factura')

    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion')

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError('El monto debe ser mayor a cero.')
        return value
