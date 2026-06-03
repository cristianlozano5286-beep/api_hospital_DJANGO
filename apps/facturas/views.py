from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Factura
from .serializers import FacturaSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar facturas', tags=['Facturas']),
    create=extend_schema(summary='Crear factura', tags=['Facturas']),
    retrieve=extend_schema(summary='Obtener factura', tags=['Facturas']),
    update=extend_schema(summary='Actualizar factura', tags=['Facturas']),
    partial_update=extend_schema(summary='Actualizar parcialmente factura', tags=['Facturas']),
    destroy=extend_schema(summary='Anular factura', tags=['Facturas']),
)
class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_factura', 'paciente__nombres', 'paciente__apellidos', 'estado']
    ordering_fields = ['fecha_emision', 'total', 'estado']
    ordering = ['-fecha_emision']

    def get_queryset(self):
        qs = Factura.objects.select_related('paciente', 'cita').prefetch_related('pagos').all()
        estado = self.request.query_params.get('estado')
        paciente = self.request.query_params.get('paciente')
        if estado:
            qs = qs.filter(estado=estado)
        if paciente:
            qs = qs.filter(paciente_id=paciente)
        activo = self.request.query_params.get('activo')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = 'anulada'
        instance.save(update_fields=['estado', 'fecha_modificacion'])
        instance.desactivar()
        return Response({'mensaje': f'Factura {instance.numero_factura} anulada.'}, status=status.HTTP_200_OK)

    @extend_schema(summary='Recalcular total de factura', tags=['Facturas'])
    @action(detail=True, methods=['post'], url_path='calcular-total')
    def calcular_total(self, request, pk=None):
        instance = self.get_object()
        instance.calcular_total()
        return Response(FacturaSerializer(instance).data)
