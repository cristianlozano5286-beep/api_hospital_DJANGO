from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Cita
from .serializers import CitaSerializer


@extend_schema_view(
    list=extend_schema(summary='Listar citas', tags=['Citas']),
    create=extend_schema(summary='Programar cita', tags=['Citas']),
    retrieve=extend_schema(summary='Obtener cita', tags=['Citas']),
    update=extend_schema(summary='Actualizar cita', tags=['Citas']),
    partial_update=extend_schema(summary='Actualizar parcialmente cita', tags=['Citas']),
    destroy=extend_schema(summary='Cancelar/desactivar cita', tags=['Citas']),
)
class CitaViewSet(viewsets.ModelViewSet):
    serializer_class = CitaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__nombres', 'paciente__apellidos', 'medico__nombres', 'estado']
    ordering_fields = ['fecha_hora', 'estado', 'fecha_creacion']
    ordering = ['-fecha_hora']

    def get_queryset(self):
        qs = Cita.objects.select_related(
            'paciente', 'medico', 'medico__especialidad'
        ).all()
        for param in ('estado', 'paciente', 'medico'):
            val = self.request.query_params.get(param)
            if val:
                qs = qs.filter(**{f'{param}__id' if param in ('paciente', 'medico') else param: val})
        activo = self.request.query_params.get('activo')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = 'cancelada'
        instance.save(update_fields=['estado', 'fecha_modificacion'])
        instance.desactivar()
        return Response({'mensaje': 'Cita cancelada.'}, status=status.HTTP_200_OK)

    @extend_schema(summary='Cambiar estado de la cita', tags=['Citas'])
    @action(detail=True, methods=['patch'], url_path='estado')
    def cambiar_estado(self, request, pk=None):
        instance = self.get_object()
        nuevo_estado = request.data.get('estado')
        estados_validos = [e[0] for e in Cita.ESTADO_CHOICES]
        if nuevo_estado not in estados_validos:
            return Response(
                {'error': f'Estado inválido. Opciones: {estados_validos}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.estado = nuevo_estado
        instance.save(update_fields=['estado', 'fecha_modificacion'])
        return Response(CitaSerializer(instance).data)
