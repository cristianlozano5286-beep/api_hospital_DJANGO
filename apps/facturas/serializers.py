from rest_framework import serializers
from .models import Factura
from apps.pacientes.serializers import PacienteSerializer


class FacturaSerializer(serializers.ModelSerializer):
    paciente_detalle = PacienteSerializer(source='paciente', read_only=True)
    saldo_pendiente = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion')

    def get_saldo_pendiente(self, obj) -> float:
        pagado = sum(p.monto for p in obj.pagos.filter(activo=True))
        return float(obj.total) - float(pagado)
