from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# 1. Creamos la vista que lista las rutas
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'citas': request.build_absolute_uri('citas/'),
        'especialidades': request.build_absolute_uri('especialidades/'),
        'facturas': request.build_absolute_uri('facturas/'),
        'medicamentos': request.build_absolute_uri('medicamentos/'),
        'medicos': request.build_absolute_uri('medicos/'),
        'pacientes': request.build_absolute_uri('pacientes/'),
        'pagos': request.build_absolute_uri('pagos/'),
        'tratamientos': request.build_absolute_uri('tratamientos/'),
    })

API_PREFIX = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Docs...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # 2. Ruta raíz que muestra la lista de apps
    path(API_PREFIX, api_root), 

    # 3. Tus rutas existentes
    path(API_PREFIX, include([
        path('citas/', include('apps.citas.urls')),
        path('especialidades/', include('apps.especialidades.urls')),
        path('facturas/', include('apps.facturas.urls')),
        path('medicamentos/', include('apps.medicamentos.urls')),
        path('medicos/', include('apps.medicos.urls')),
        path('pacientes/', include('apps.pacientes.urls')),
        path('pagos/', include('apps.pagos.urls')),
        path('tratamientos/', include('apps.tratamientos.urls')),
    ])),
]