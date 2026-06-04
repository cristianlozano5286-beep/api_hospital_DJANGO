from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.utils.mixins import ExportPDFMixin
from .models import Medicamento
from .serializers import MedicamentoSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar medicamentos', tags=['Medicamentos']),
    create=extend_schema(summary='Crear medicamento', tags=['Medicamentos']),
    retrieve=extend_schema(summary='Obtener medicamento', tags=['Medicamentos']),
    update=extend_schema(summary='Actualizar medicamento', tags=['Medicamentos']),
    partial_update=extend_schema(summary='Actualizar parcialmente medicamento', tags=['Medicamentos']),
    destroy=extend_schema(summary='Desactivar medicamento', tags=['Medicamentos']),
    exportar_pdf=extend_schema(summary="Exportar a PDF", tags=['Medicamentos']),
)
class MedicamentoViewSet(ExportPDFMixin, viewsets.ModelViewSet):
    serializer_class = MedicamentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre_generico', 'nombre_comercial', 'codigo_registro', 'laboratorio']
    ordering_fields = ['nombre_generico', 'precio_unitario', 'stock']
    ordering = ['nombre_generico']

    def get_queryset(self):
        qs = Medicamento.objects.all()
        activo = self.request.query_params.get('activo')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.desactivar()
        return Response({'mensaje': f'Medicamento "{instance.nombre_generico}" desactivado.'}, status=status.HTTP_200_OK)

    @extend_schema(summary='Activar medicamento', tags=['Medicamentos'])
    @action(detail=True, methods=['patch'], url_path='activar')
    def activar(self, request, pk=None):
        instance = self.get_object()
        instance.activar()
        return Response(MedicamentoSerializer(instance).data)
