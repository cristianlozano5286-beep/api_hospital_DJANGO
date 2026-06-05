from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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

urlpatterns = [
    path('admin/v1/', admin.site.urls),
    
    # Rutas de API y Documentación
    path('api/v1/', api_root),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas de las Apps (sin prefijo duplicado)
    path('api/v1/citas/', include('apps.citas.urls')),
    path('api/v1/especialidades/', include('apps.especialidades.urls')),
    path('api/v1/facturas/', include('apps.facturas.urls')),
    path('api/v1/medicamentos/', include('apps.medicamentos.urls')),
    path('api/v1/medicos/', include('apps.medicos.urls')),
    path('api/v1/pacientes/', include('apps.pacientes.urls')),
    path('api/v1/pagos/', include('apps.pagos.urls')),
    path('api/v1/tratamientos/', include('apps.tratamientos.urls')),
]