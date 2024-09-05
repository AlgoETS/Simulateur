from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .views import SearchChartView, StrategyManagementView, SandboxView
from .api import SearchAPIView, StrategyAPIView, FMPDataAPIVIewSync, CoinGeckoDataAPIViewSync, YFinanceDataAPIViewSync

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Backtesting API",
        default_version='v1',
        description="API documentation for the Backtesting project",
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
    path('sandbox/', SandboxView.as_view(), name='sandbox'),
]


api_patterns = [
    path('search-chart/', SearchAPIView.as_view(), name='api_search_chart'),
    path('strategies/', StrategyAPIView.as_view(), name='api_strategies'),
    path('data/fmp/<str:ticker>/', FMPDataAPIVIewSync.as_view(), name='api_fmp_data'),
    path('data/coingecko/<str:crypto_id>/', CoinGeckoDataAPIViewSync.as_view(), name='api_coingecko_data'),
    path('data/yfinance/<str:ticker>/', YFinanceDataAPIViewSync.as_view(), name='api_yfinance_data'),
]


urlpatterns = [
    path('', include(api_patterns)),
    # Swagger and ReDoc URLs at the top level
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(html_patterns)),
]