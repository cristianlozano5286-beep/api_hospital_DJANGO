from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Pago
from .serializers import PagoSerializer
from apps.utils.mixins import ExportExcelMixin

@extend_schema_view(
    list=extend_schema(summary='Listar pagos', tags=['Pagos']),
    exportar_excel=extend_schema(
        summary="Exportar a Excel", 
        tags=['Pagos'],
        
    ),
)
class PagoViewSet(ExportExcelMixin, viewsets.ModelViewSet):
    serializer_class = PagoSerializer
    
    # 1. ORDENAMIENTO: Siempre veremos los más recientes primero
    queryset = Pago.objects.all().order_by('-fecha_creacion')
    
    # 2. FILTROS: Opcional, te permite buscar por referencia o estado desde la URL
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['referencia_pago', 'estado']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 3. Lógica de desactivación lógica (Soft Delete)
        instance.desactivar() 
        return Response(
            {'mensaje': f'El pago {instance.id} ha sido desactivado correctamente.'}, 
            status=status.HTTP_200_OK
        )