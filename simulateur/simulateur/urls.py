from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from pictures.conf import get_settings
from simulation.urls import urlpatterns as simulation_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Simulateur API",
        default_version='v1',
        description="API documentation for the Simulateur project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="antoine@antoineboucher.info"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
                  path('jet/', include('jet.urls', 'jet')),
                  path('tinymce/', include('tinymce.urls')),
                  path('admin/', admin.site.urls),
                  path('api/', include(simulation_urls)),
                  path('accounts/', include('allauth.urls')),
                  path("django-check-seo/", include("django_check_seo.urls")),
                  path('', include(simulation_urls)),
                  path('', include('django_prometheus.urls')),
                  path('', include('guest_user.urls')),
                  path('', include('pwa.urls')),
                  path('health', include('health_check.urls')),

                  # Swagger and ReDoc URLs
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)

if get_settings().USE_PLACEHOLDERS:
    urlpatterns += [
        path("_pictures/", include("pictures.urls")),
    ]