from rest_framework import serializers
from .models import Pacientes # Importa los modelos que necesites

class PacientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacientes
        fields = '__all__'