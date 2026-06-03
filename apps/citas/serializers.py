from rest_framework import serializers
from .models import Cita
from apps.pacientes.serializers import PacienteSerializer
from apps.medicos.serializers import MedicoSerializer


class CitaSerializer(serializers.ModelSerializer):
    paciente_detalle = PacienteSerializer(source='paciente', read_only=True)
    medico_detalle = MedicoSerializer(source='medico', read_only=True)

    class Meta:
        model = Cita
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion')

    def validate(self, data):
        # Verificar que el médico esté activo
        medico = data.get('medico')
        if medico and not medico.activo:
            raise serializers.ValidationError({'medico': 'El médico seleccionado no está activo.'})
        paciente = data.get('paciente')
        if paciente and not paciente.activo:
            raise serializers.ValidationError({'paciente': 'El paciente seleccionado no está activo.'})
        return data
