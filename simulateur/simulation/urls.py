# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from simulation.api.scenario import CreateScenario, PublishScenario
from simulation.api.auth import JoinTeam, RemoveTeamMember

# Importing HTML views
from simulation.views.dashboard import GameDashboardView, HomeView, PortfolioDetailView, PortfolioUserDetailView, UserDashboardView, AdminDashboardView, TeamDashboardView, MarketOverviewView
from simulation.views.auth import ForgotPasswordView, LogoutView, PasswordResetConfirmView, PrivateProfileView, PublicProfileView, SettingsView, SignupView, LoginView, JoinTeamView
from simulation.views.simulation import SimulationGraphView
# Importing API views
from simulation.api.simulation import SimulationSettingsView, StartSimulation, PauseSimulation, StopSimulation, FastForwardSimulation, RewindSimulation
from simulation.api.portfolio import BuyStock, PortfolioView, SellStock
from simulation.api.scenario import ScenarioStocks, StockHistory, GetPublishedScenarios, CreateCompanyAndStock, CreateNews, CreateEvent, CreateTrigger
from simulation.api.ai_llm import InteractWithOllama, CreateNewsAI, CreateEventAI, CreateTriggerAI, CreateCompanyAndStockAI, CreateScenarioAI
from simulation.api.auth import JoinTeam, RemoveTeamMember, UpdateTeamName, UpdateMemberRole

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
    path('profile/', PrivateProfileView.as_view(), name='private_profile'),  # Private profile
    path('profile/<int:user_id>/', PublicProfileView.as_view(), name='public_profile'),  # Public profile
    path('settings/', SettingsView.as_view(), name='settings'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('join_team/', JoinTeamView.as_view(), name='join_team'),
    path('portfolio/<int:portfolio_id>/', PortfolioDetailView.as_view(), name='portfolio_detail'),  # Portfolio detail view
    path('portfolio/', PortfolioUserDetailView.as_view(), name='portfolio_detail'),  # Portfolio detail view
]

api_patterns = [
    path('simulation/start/', StartSimulation.as_view(), name='start_simulation'),
    path('simulation/pause/', PauseSimulation.as_view(), name='pause_simulation'),
    path('simulation/stop/', StopSimulation.as_view(), name='stop_simulation'),
    path('simulation/fast-forward/', FastForwardSimulation.as_view(), name='fast-forward-simulation'),
    path('simulation/rewind/', RewindSimulation.as_view(), name='rewind-simulation'),
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='portfolio_view'),
    path('stock/buy/', BuyStock.as_view(), name='buy_stock'),
    path('stock/sell/', SellStock.as_view(), name='sell_stock'),
    path('graph/', SimulationGraphView.as_view(), name='simulation_graph'),
    path('settings/', SimulationSettingsView.as_view(), name='simulation_settings'),
    path('join_team/<int:team_id>/<str:key>/', JoinTeam.as_view(), name='join_team'),
    path('team/remove-member/<int:team_id>/<int:user_id>/', RemoveTeamMember.as_view(), name='remove_team_member'),
    path('team/update-name/<int:team_id>/', UpdateTeamName.as_view(), name='change_team_name'),
    path('team/update-role/<int:team_id>/<int:user_id>/', UpdateMemberRole.as_view(), name='update_member_role'),
    path('scenario/create/', CreateScenario.as_view(), name='create_scenario'),
    path('scenario/publish/<int:scenario_id>/', PublishScenario.as_view(), name='publish_scenario'),
    path('scenarios/published/', GetPublishedScenarios.as_view(), name='get_published_scenarios'),
    path('scenarios/<int:scenario_id>/stocks/', ScenarioStocks.as_view(), name='scenario_stocks'),
    path('stocks/<int:stock_id>/history/', StockHistory.as_view(), name='stock_history'),
    path('scenario/company-and-stock/', CreateCompanyAndStock.as_view(), name='create_company_and_stock'),
    path('scenario/news/', CreateNews.as_view(), name='create_news'),
    path('scenario/event/', CreateEvent.as_view(), name='create_event'),
    path('scenario/trigger/', CreateTrigger.as_view(), name='create_trigger'),
    path('interact-with-ollama/', InteractWithOllama.as_view(), name='interact-with-ollama'),
    path('create-news-ai/', CreateNewsAI.as_view(), name='create-news-ai'),
    path('create-event-ai/', CreateEventAI.as_view(), name='create-event-ai'),
    path('create-trigger-ai/', CreateTriggerAI.as_view(), name='create-trigger-ai'),
    path('create-company-stock-ai/', CreateCompanyAndStockAI.as_view(), name='create-company-stock-ai'),
    path('create-scenario-ai/', CreateScenarioAI.as_view(), name='create-scenario-ai'),

]

# Combine both HTML and API patterns into a single list
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(api_patterns)),
    path('', include(html_patterns)),
]
