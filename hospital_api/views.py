from rest_framework import generics
from .models import Pacientes
from .serializers import PacientesSerializer

class PacientesList(generics.ListAPIView):
    queryset = Pacientes.objects.all()
    serializer_class = PacientesSerializer