from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Pago
from .serializers import PagoSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar pagos', tags=['Pagos']),
    create=extend_schema(summary='Registrar pago', tags=['Pagos']),
    retrieve=extend_schema(summary='Obtener pago', tags=['Pagos']),
    update=extend_schema(summary='Actualizar pago', tags=['Pagos']),
    partial_update=extend_schema(summary='Actualizar parcialmente pago', tags=['Pagos']),
    destroy=extend_schema(summary='Desactivar pago', tags=['Pagos']),
)
class PagoViewSet(viewsets.ModelViewSet):
    serializer_class = PagoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['factura__numero_factura', 'referencia_pago', 'metodo_pago', 'estado']
    ordering_fields = ['fecha_pago', 'monto', 'estado']
    ordering = ['-fecha_pago']

    def get_queryset(self):
        qs = Pago.objects.select_related('factura', 'factura__paciente').all()
        factura = self.request.query_params.get('factura')
        estado = self.request.query_params.get('estado')
        if factura:
            qs = qs.filter(factura_id=factura)
        if estado:
            qs = qs.filter(estado=estado)
        activo = self.request.query_params.get('activo')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.desactivar()
        return Response({'mensaje': f'Pago {instance.id} desactivado.'}, status=status.HTTP_200_OK)
