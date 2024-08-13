from django.urls import path, include
from rest_framework.routers import DefaultRouter
from simulation.api.ai_llm import (
    InteractWithOllama,
    CreateNewsAI,
    CreateEventAI,
    CreateTriggerAI,
    CreateCompanyAndStockAI,
    CreateScenarioAI,
)
from simulation.api.auth import UpdateMemberRole
from simulation.api.portfolio import (
    BuyStock,
    PortfolioView,
    SellStock,
    StockPrice,
    UserOrders,
)
from simulation.api.teams import GenerateJoinLink, JoinTeam, RemoveTeamMember, UpdateTeamName
from simulation.views.auth import (
    ForgotPasswordView,
    LogoutView,
    PasswordResetConfirmView,
    PrivateProfileView,
    PublicProfileView,
    SettingsView,
    SignupView,
    LoginView,
    JoinTeamView,
)
# Importing HTML views
from simulation.views.dashboard import (
    GameDashboardView,
    HomeView,
    PortfolioDetailView,
    PortfolioUserDetailView,
    UserDashboardView,
    AdminDashboardView,
    TeamDashboardView,
    MarketOverviewView,
)
from simulation.api.event import (
    EventManagement
)

from simulation.api.news import NewsManagement
from simulation.api.trigger import TriggerManagement

router = DefaultRouter()

html_patterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('dashboard/admin', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/team', TeamDashboardView.as_view(), name='team_dashboard'),
    path('dashboard/game', GameDashboardView.as_view(), name='game_dashboard'),
    path('market/overview/', MarketOverviewView.as_view(), name='market_overview'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', PrivateProfileView.as_view(), name='private_profile'),
    path('profile/<int:user_id>/', PublicProfileView.as_view(), name='public_profile'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('join_team/', JoinTeamView.as_view(), name='join_team'),
    path('portfolio/<int:portfolio_id>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('portfolio/', PortfolioUserDetailView.as_view(), name='portfolio_detail'),
]

api_patterns = [
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='portfolio_view'),
    path('stock/buy/', BuyStock.as_view(), name='buy_stock'),
    path('stock/sell/', SellStock.as_view(), name='sell_stock'),
    path('stock/price/<stock_id>/', StockPrice.as_view(), name='stock_price'),
    path('user/orders/', UserOrders.as_view(), name='user_orders'),
    path('join_team/<int:team_id>/<str:key>/', JoinTeam.as_view(), name='join_team'),
    path('team/remove-member/<int:team_id>/<int:user_id>/', RemoveTeamMember.as_view(), name='remove_team_member'),
    path('team/update-name/<int:team_id>/', UpdateTeamName.as_view(), name='change_team_name'),
    path('team/update-role/<int:team_id>/<int:user_id>/', UpdateMemberRole.as_view(), name='update_member_role'),
    path('interact-with-ollama/', InteractWithOllama.as_view(), name='interact-with-ollama'),
    path('create-news-ai/', CreateNewsAI.as_view(), name='create-news-ai'),
    path('create-event-ai/', CreateEventAI.as_view(), name='create-event-ai'),
    path('create-trigger-ai/', CreateTriggerAI.as_view(), name='create-trigger-ai'),
    path('create-company-stock-ai/', CreateCompanyAndStockAI.as_view(), name='create-company-stock-ai'),
    path('create-scenario-ai/', CreateScenarioAI.as_view(), name='create-scenario-ai'),
    path('team/generate-join-link/<int:team_id>/', GenerateJoinLink.as_view(), name='generate_join_link'),

    path('/news/', NewsManagement.as_view(), name='create_news'),
    path('/news/<int:news_id>/', NewsManagement.as_view(), name='manage_news'),
    path('event/', EventManagement.as_view(), name='create_event'),
    path('event/<int:event_id>/', EventManagement.as_view(), name='manage_event'),
    path('triggers/', TriggerManagement.as_view(), name='create_trigger'),
    path('triggers/<int:trigger_id>/', TriggerManagement.as_view(), name='manage_trigger'),
]
# Combine both HTML and API patterns into a single list
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(api_patterns)),
    path('', include(html_patterns)),
]
