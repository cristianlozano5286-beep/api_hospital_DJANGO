from rest_framework import serializers
from .models import Medico
from apps.especialidades.serializers import EspecialidadSerializer


class MedicoSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()
    especialidad_detalle = EspecialidadSerializer(source='especialidad', read_only=True)

    class Meta:
        model = Medico
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['especialidad_detalle'] = EspecialidadSerializer(instance.especialidad).data
        return rep
