from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from .views import SearchChartView, StrategyManagementView
from .api import ChartSearchAPIView, StrategyAPIView

# Swagger Schema View
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

# HTML view patterns
html_patterns = [
    path('search-chart/', SearchChartView.as_view(), name='search_chart'),
    path('strategy-management/', StrategyManagementView.as_view(), name='strategy_management'),
]


api_patterns = [
    path('api/search-chart/', ChartSearchAPIView.as_view(), name='api_search_chart'),
    path('api/strategies/', StrategyAPIView.as_view(), name='api_strategies'),
    path('fmp-data/<str:ticker>/', FMPDataAPIView.as_view(), name='fmp_data')
]


urlpatterns = [
    path('api/', include(api_patterns)),
    # Swagger and ReDoc URLs at the top level
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(html_patterns)),
]