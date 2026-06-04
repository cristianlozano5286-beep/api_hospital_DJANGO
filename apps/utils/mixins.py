from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BaseRenderer
from drf_spectacular.utils import extend_schema
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string


class PDFRenderer(BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class ExportPDFMixin:
    @extend_schema(summary="Exportar a PDF", tags=['Exportación'])
    @action(detail=True, methods=['get'], renderer_classes=[PDFRenderer])
    @permission_classes([AllowAny])
    def exportar_pdf(self, request, pk=None):
        instance = self.get_object()
        modelo_nombre = instance._meta.model_name
        template_path = f'{modelo_nombre}/reporte.html'
        html_string = render_to_string(template_path, {'object': instance})
        pdf = HTML(string=html_string).write_pdf()
        return Response(pdf, content_type='application/pdf', headers={'Content-Disposition': f'attachment; filename="{modelo_nombre}_{instance.pk}.pdf"'})