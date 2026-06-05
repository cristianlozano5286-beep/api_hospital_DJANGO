from rest_framework import serializers
from .models import Medicamento


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion')
