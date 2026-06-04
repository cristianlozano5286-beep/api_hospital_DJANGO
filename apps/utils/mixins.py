from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

class ExportPDFMixin:
    @extend_schema(summary="Exportar a PDF", tags=['Exportación'])
    @action(detail=True, methods=['get'])
    def exportar_pdf(self, request, pk=None):
        instance = self.get_object()
        modelo_nombre = instance._meta.model_name
        template_path = f'{modelo_nombre}/reporte.html'
        html_string = render_to_string(template_path, {modelo_nombre: instance})
        pdf = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{modelo_nombre}_{instance.pk}.pdf"'
        return response