from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()

    class Meta:
        model = Paciente
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion')
