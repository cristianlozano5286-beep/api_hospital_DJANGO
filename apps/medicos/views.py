from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.utils.mixins import ExportPDFMixin
from .models import Medico
from .serializers import MedicoSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar médicos', tags=['Médicos']),
    create=extend_schema(summary='Crear médico', tags=['Médicos']),
    retrieve=extend_schema(summary='Obtener médico', tags=['Médicos']),
    update=extend_schema(summary='Actualizar médico', tags=['Médicos']),
    partial_update=extend_schema(summary='Actualizar parcialmente médico', tags=['Médicos']),
    destroy=extend_schema(summary='Desactivar médico', tags=['Médicos']),
    exportar_pdf=extend_schema(summary="Exportar a PDF", tags=['Médicos']),
)
class MedicoViewSet(ExportPDFMixin, viewsets.ModelViewSet):
    """CRUD completo para médicos del sistema hospitalario."""

    serializer_class = MedicoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombres', 'apellidos', 'documento_identidad', 'numero_registro', 'correo_electronico']
    ordering_fields = ['apellidos', 'nombres', 'fecha_creacion', 'anos_experiencia']
    ordering = ['apellidos']

    def get_queryset(self):
        qs = Medico.objects.select_related('especialidad').all()
        activo = self.request.query_params.get('activo')
        especialidad = self.request.query_params.get('especialidad')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        if especialidad:
            qs = qs.filter(especialidad_id=especialidad)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.desactivar()
        return Response(
            {'mensaje': f'Médico "{instance.nombre_completo}" desactivado correctamente.'},
            status=status.HTTP_200_OK,
        )

    @extend_schema(summary='Activar médico', tags=['Médicos'])
    @action(detail=True, methods=['patch'], url_path='activar')
    def activar(self, request, pk=None):
        instance = self.get_object()
        instance.activar()
        return Response(MedicoSerializer(instance).data)
