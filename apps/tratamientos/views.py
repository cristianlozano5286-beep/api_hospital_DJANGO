from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Tratamiento
from .serializers import TratamientoSerializer
from apps.utils.mixins import ExportPDFMixin


@extend_schema_view(
    list=extend_schema(summary='Listar tratamientos', tags=['Tratamientos']),
    create=extend_schema(summary='Crear tratamiento', tags=['Tratamientos']),
    retrieve=extend_schema(summary='Obtener tratamiento', tags=['Tratamientos']),
    update=extend_schema(summary='Actualizar tratamiento', tags=['Tratamientos']),
    partial_update=extend_schema(summary='Actualizar parcialmente tratamiento', tags=['Tratamientos']),
    destroy=extend_schema(summary='Desactivar tratamiento', tags=['Tratamientos']),
    exportar_pdf=extend_schema(summary="Exportar a PDF", tags=['Tratamientos']),
)
class TratamientoViewSet(ExportPDFMixin, viewsets.ModelViewSet):
    serializer_class = TratamientoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['medicamento__nombre_generico', 'cita__paciente__apellidos']
    ordering_fields = ['fecha_creacion', 'duracion_dias', 'costo_tratamiento']
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        qs = Tratamiento.objects.select_related(
            'cita', 'cita__paciente', 'medicamento'
        ).all()
        cita = self.request.query_params.get('cita')
        if cita:
            qs = qs.filter(cita_id=cita)
        activo = self.request.query_params.get('activo')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.desactivar()
        return Response({'mensaje': 'Tratamiento desactivado.'}, status=status.HTTP_200_OK)
