from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Paciente
from .serializers import PacienteSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar pacientes', tags=['Pacientes']),
    create=extend_schema(summary='Registrar paciente', tags=['Pacientes']),
    retrieve=extend_schema(summary='Obtener paciente', tags=['Pacientes']),
    update=extend_schema(summary='Actualizar paciente', tags=['Pacientes']),
    partial_update=extend_schema(summary='Actualizar parcialmente paciente', tags=['Pacientes']),
    destroy=extend_schema(summary='Desactivar paciente', tags=['Pacientes']),
)
class PacienteViewSet(viewsets.ModelViewSet):
    serializer_class = PacienteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombres', 'apellidos', 'documento_identidad', 'correo_electronico', 'eps']
    ordering_fields = ['apellidos', 'nombres', 'fecha_nacimiento', 'fecha_creacion']
    ordering = ['apellidos']

    def get_queryset(self):
        qs = Paciente.objects.all()
        activo = self.request.query_params.get('activo')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.desactivar()
        return Response(
            {'mensaje': f'Paciente "{instance.nombre_completo}" desactivado.'},
            status=status.HTTP_200_OK,
        )

    @extend_schema(summary='Activar paciente', tags=['Pacientes'])
    @action(detail=True, methods=['patch'], url_path='activar')
    def activar(self, request, pk=None):
        instance = self.get_object()
        instance.activar()
        return Response(PacienteSerializer(instance).data)

    @extend_schema(summary='Historial de citas del paciente', tags=['Pacientes'])
    @action(detail=True, methods=['get'], url_path='citas')
    def citas(self, request, pk=None):
        from apps.citas.models import Cita
        from apps.citas.serializers import CitaSerializer
        paciente = self.get_object()
        citas = Cita.objects.filter(paciente=paciente).select_related('medico', 'medico__especialidad')
        return Response(CitaSerializer(citas, many=True).data)
