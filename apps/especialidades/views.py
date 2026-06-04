from django.template.loader import render_to_string
import traceback
from django.http import HttpResponse
from weasyprint import HTML
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BaseRenderer
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Especialidad
from .serializers import EspecialidadSerializer
from django.shortcuts import get_object_or_404


class PDFRenderer(BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

@extend_schema_view(
    list=extend_schema(summary='Listar especialidades', tags=['Especialidades']),
    create=extend_schema(summary='Crear especialidad', tags=['Especialidades']),
    retrieve=extend_schema(summary='Obtener especialidad', tags=['Especialidades']),
    update=extend_schema(summary='Actualizar especialidad', tags=['Especialidades']),
    partial_update=extend_schema(summary='Actualizar parcialmente especialidad', tags=['Especialidades']),
    destroy=extend_schema(summary='Eliminar especialidad', tags=['Especialidades']),
    exportar_pdf=extend_schema(summary="Exportar a PDF", tags=['Especialidades']),
)
class EspecialidadViewSet(viewsets.ModelViewSet):
    serializer_class = EspecialidadSerializer
    queryset = Especialidad.objects.all() # Es mejor definir el queryset aquí
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'codigo', 'fecha_creacion']
    ordering = ['nombre']

    @action(detail=True, methods=['get'], renderer_classes=[PDFRenderer], url_path='exportar_pdf')
    @permission_classes([AllowAny])
    def exportar_pdf(self, request, pk=None):
        try:
            instance = self.get_object()
            template_path = 'especialidad/reporte.html'
            html_string = render_to_string(template_path, {'object': instance})
            pdf = HTML(string=html_string).write_pdf()
            
            return Response(pdf, content_type='application/pdf', headers={'Content-Disposition': 'attachment; filename="reporte.pdf"'})
        except Exception as e:
            error_detalle = traceback.format_exc()
            print(f"--- ERROR CRÍTICO: {error_detalle} ---")
            return Response(f"ERROR: {error_detalle}", status=500)

    def get_queryset(self):
        qs = Especialidad.objects.all()
        activo = self.request.query_params.get('activo')
        if activo is not None:
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.desactivar()
        return Response({'mensaje': f'Especialidad "{instance.nombre}" desactivada.'}, status=status.HTTP_200_OK)

    @extend_schema(summary='Activar especialidad', tags=['Especialidades'])
    @action(detail=True, methods=['patch'], url_path='activar')
    def activar(self, request, pk=None):
        instance = self.get_object()
        instance.activar()
        return Response(EspecialidadSerializer(instance).data)