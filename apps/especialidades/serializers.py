from rest_framework import serializers
from .models import Especialidad


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion')
