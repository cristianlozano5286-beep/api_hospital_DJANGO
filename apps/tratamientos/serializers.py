from rest_framework import serializers
from .models import Tratamiento
from apps.medicamentos.serializers import MedicamentoSerializer


class TratamientoSerializer(serializers.ModelSerializer):
    medicamento_detalle = MedicamentoSerializer(source='medicamento', read_only=True)

    class Meta:
        model = Tratamiento
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion')

    def validate_medicamento(self, value):
        if not value.activo:
            raise serializers.ValidationError('El medicamento seleccionado no está activo.')
        return value
