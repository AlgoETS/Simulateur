from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from pictures.conf import get_settings

# Adjust the import statement if simulateur and simulation are separate apps
from simulation.urls import urlpatterns as simulation_urls

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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if get_settings().USE_PLACEHOLDERS:
    urlpatterns += [
        path("_pictures/", include("pictures.urls")),
    ]