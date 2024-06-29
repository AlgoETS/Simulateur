# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from simulation.api.scenario import CreateScenario, PublishScenario
from simulation.api.auth import JoinTeam

# Importing HTML views
from simulation.views.dashboard import GameDashboardView, HomeView, PortfolioDetailView, PortfolioUserDetailView, UserDashboardView, AdminDashboardView, TeamDashboardView, MarketOverviewView
from simulation.views.auth import ForgotPasswordView, LogoutView, PasswordResetConfirmView, PrivateProfileView, PublicProfileView, SettingsView, SignupView, LoginView, JoinTeamView
=======
from simulation.api.auth import JoinTeamView
from simulation.api.data_modification import SimulationDataViewSet
from simulation.api.trigger import TriggerViewSet

# Importing HTML views
from simulation.views.dashboard import GameDashboardView, HomeView, UserDashboardView, AdminDashboardView, TeamDashboardView, MarketOverviewView, BuySellView
from simulation.views.auth import LogoutView, ProfileView, SettingsView, SignupView, LoginView
>>>>>>> origin/main
from simulation.views.simulation import SimulationGraphView
# Importing API views
from simulation.api.simulation import SimulationSettingsView, StartSimulation, PauseSimulation, StopSimulation, FastForwardSimulation, RewindSimulation
from simulation.api.portfolio import BuyStock, PortfolioView, SellStock
from simulation.api.scenario import ScenarioStocks, StockHistory, GetPublishedScenarios

router = DefaultRouter()
<<<<<<< HEAD
=======
router.register(r'companies', CompanyViewSet)
router.register(r'scenarios', ScenarioViewSet)
router.register(r'events', EventViewSet)
router.register(r'triggers', TriggerViewSet)
router.register(r'simulation_data', SimulationDataViewSet)
>>>>>>> origin/main

html_patterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
<<<<<<< HEAD
    path('dashboard/admin', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/team', TeamDashboardView.as_view(), name='team_dashboard'),
    path('dashboard/game', GameDashboardView.as_view(), name='game_dashboard'),
=======
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('team/dashboard/', TeamDashboardView.as_view(), name='team_dashboard'),
    path('game/dashboard/', GameDashboardView.as_view(), name='game_dashboard'),
>>>>>>> origin/main
    path('market/overview/', MarketOverviewView.as_view(), name='market_overview'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
<<<<<<< HEAD
    path('profile/', PrivateProfileView.as_view(), name='private_profile'),  # Private profile
    path('profile/<int:user_id>/', PublicProfileView.as_view(), name='public_profile'),  # Public profile
    path('settings/', SettingsView.as_view(), name='settings'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('join_team/', JoinTeamView.as_view(), name='join_team'),
    path('portfolio/<int:portfolio_id>/', PortfolioDetailView.as_view(), name='portfolio_detail'),  # Portfolio detail view
    path('portfolio/', PortfolioUserDetailView.as_view(), name='portfolio_detail'),  # Portfolio detail view
=======
    path('profile/', ProfileView.as_view(), name='profile'),
    path('settings/', SettingsView.as_view(), name='settings'),
>>>>>>> origin/main
]

api_patterns = [
    path('simulation/start/', StartSimulation.as_view(), name='start_simulation'),
    path('simulation/pause/', PauseSimulation.as_view(), name='pause_simulation'),
    path('simulation/stop/', StopSimulation.as_view(), name='stop_simulation'),
    path('simulation/fast-forward/', FastForwardSimulation.as_view(), name='fast-forward-simulation'),
    path('simulation/rewind/', RewindSimulation.as_view(), name='rewind-simulation'),
<<<<<<< HEAD
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='portfolio_view'),
    path('stock/buy/', BuyStock.as_view(), name='buy_stock'),
    path('stock/sell/', SellStock.as_view(), name='sell_stock'),
    path('graph/', SimulationGraphView.as_view(), name='simulation_graph'),
    path('settings/', SimulationSettingsView.as_view(), name='simulation_settings'),
    path('join-team/<int:team_id>/<str:key>/', JoinTeam.as_view(), name='join_team'),
    path('scenario/create/', CreateScenario.as_view(), name='create_scenario'),
    path('scenario/publish/<int:scenario_id>/', PublishScenario.as_view(), name='publish_scenario'),
    path('scenarios/published/', GetPublishedScenarios.as_view(), name='get_published_scenarios'),
    path('scenarios/<int:scenario_id>/stocks/', ScenarioStocks.as_view(), name='scenario_stocks'),
    path('stocks/<int:stock_id>/history/', StockHistory.as_view(), name='stock_history'),
=======
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='portfolio-view'),
    path('stock/buy/', BuyStock.as_view(), name='buy-stock'),
    path('stock/sell/', SellStock.as_view(), name='sell-stock'),
    path('graph/', SimulationGraphView.as_view(), name='simulation-graph'),
    path('settings/', SimulationSettingsView.as_view(), name='simulation-settings'),
    path('join-team/<int:team_id>/<str:key>/', JoinTeamView.as_view(), name='join_team'),
>>>>>>> origin/main
]

# Combine both HTML and API patterns into a single list
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(api_patterns)),
    path('', include(html_patterns)),
]
