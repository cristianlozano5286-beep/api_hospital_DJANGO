from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.utils.mixins import ExportPDFMixin
from .models import Especialidad
from .serializers import EspecialidadSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar especialidades', tags=['Especialidades']),
    create=extend_schema(summary='Crear especialidad', tags=['Especialidades']),
    retrieve=extend_schema(summary='Obtener especialidad', tags=['Especialidades']),
    update=extend_schema(summary='Actualizar especialidad', tags=['Especialidades']),
    partial_update=extend_schema(summary='Actualizar parcialmente especialidad', tags=['Especialidades']),
    destroy=extend_schema(summary='Eliminar especialidad', tags=['Especialidades']),
    exportar_pdf=extend_schema(summary="Exportar a PDF", tags=['Especialidades']),
)
class EspecialidadViewSet(ExportPDFMixin, viewsets.ModelViewSet):
    """CRUD completo para especialidades médicas."""

    serializer_class = EspecialidadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'codigo', 'fecha_creacion']
    ordering = ['nombre']

    def get_queryset(self):
        qs = Especialidad.objects.all()
        activo = self.request.query_params.get('activo')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs

    def destroy(self, request, *args, **kwargs):
        """Soft-delete: desactiva en lugar de eliminar."""
        instance = self.get_object()
        instance.desactivar()
        return Response(
            {'mensaje': f'Especialidad "{instance.nombre}" desactivada correctamente.'},
            status=status.HTTP_200_OK,
        )

    @extend_schema(summary='Activar especialidad desactivada', tags=['Especialidades'])
    @action(detail=True, methods=['patch'], url_path='activar')
    def activar(self, request, pk=None):
        instance = self.get_object()
        instance.activar()
        return Response(EspecialidadSerializer(instance).data)
