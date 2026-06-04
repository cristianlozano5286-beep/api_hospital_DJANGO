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
    path('admin/', admin.site.urls),
    
    # Rutas de API y Documentación
    path('api/', api_root),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas de las Apps (sin prefijo duplicado)
    path('api/citas/', include('apps.citas.urls')),
    path('api/especialidades/', include('apps.especialidades.urls')),
    path('api/facturas/', include('apps.facturas.urls')),
    path('api/medicamentos/', include('apps.medicamentos.urls')),
    path('api/medicos/', include('apps.medicos.urls')),
    path('api/pacientes/', include('apps.pacientes.urls')),
    path('api/pagos/', include('apps.pagos.urls')),
    path('api/tratamientos/', include('apps.tratamientos.urls')),
]