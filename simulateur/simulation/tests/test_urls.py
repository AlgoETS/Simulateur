from django.test import SimpleTestCase
from django.urls import reverse, resolve
from simulation.api.auth import UpdateMemberRole
from simulation.api.portfolio import (
    BuyStock,
    SellStock,
    StockPrice,
    PortfolioView,
)
from simulation.api.teams import GenerateJoinLink, JoinTeam, RemoveTeamMember, UpdateTeamName
from simulation.api.ai_llm import (
    InteractWithOllama,
    CreateNewsAI,
    CreateEventAI,
    CreateTriggerAI,
    CreateCompanyAndStockAI,
    CreateScenarioAI,
)
from simulation.api.company import CompanyManagement
from simulation.api.scenario import ScenarioManagement
from simulation.api.scenario_manager import (
    ScenarioManagerManagement, ChangeScenarioManagerState, ScenarioManagerNews,
    ScenarioManagerTriggers, ScenarioManagerEvents, ScenarioManagerStocks, ScenarioManagerTeams
)
from simulation.api.event import EventManagement
from simulation.api.news import NewsManagement
from simulation.api.trigger import TriggerManagement
from simulation.api.transaction import UserOrders
from simulation.api.stock import StockManagement, StockPriceHistoryManagement

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

class UrlsTest(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_user_dashboard_url_is_resolved(self):
        url = reverse('user_dashboard')
        self.assertEqual(resolve(url).func.view_class, UserDashboardView)

    def test_admin_dashboard_url_is_resolved(self):
        url = reverse('admin_dashboard')
        self.assertEqual(resolve(url).func.view_class, AdminDashboardView)

    def test_team_dashboard_url_is_resolved(self):
        url = reverse('team_dashboard')
        self.assertEqual(resolve(url).func.view_class, TeamDashboardView)

    def test_game_dashboard_url_is_resolved(self):
        url = reverse('game_dashboard')
        self.assertEqual(resolve(url).func.view_class, GameDashboardView)

    def test_market_overview_url_is_resolved(self):
        url = reverse('market_overview')
        self.assertEqual(resolve(url).func.view_class, MarketOverviewView)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignupView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_private_profile_url_is_resolved(self):
        url = reverse('private_profile')
        self.assertEqual(resolve(url).func.view_class, PrivateProfileView)

    def test_public_profile_url_is_resolved(self):
        url = reverse('public_profile', kwargs={'user_id': 1})
        self.assertEqual(resolve(url).func.view_class, PublicProfileView)

    def test_settings_url_is_resolved(self):
        url = reverse('settings')
        self.assertEqual(resolve(url).func.view_class, SettingsView)

    def test_forgot_password_url_is_resolved(self):
        url = reverse('forgot_password')
        self.assertEqual(resolve(url).func.view_class, ForgotPasswordView)

    def test_password_reset_confirm_url_is_resolved(self):
        url = reverse('password_reset_confirm', kwargs={'uidb64': 'uid', 'token': 'token'})
        self.assertEqual(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_join_team_url_is_resolved(self):
        url = reverse('join_team')
        self.assertEqual(resolve(url).func.view_class, JoinTeamView)

    def test_portfolio_detail_url_is_resolved(self):
        url = reverse('portfolio_detail', kwargs={'portfolio_id': 1})
        self.assertEqual(resolve(url).func.view_class, PortfolioDetailView)

    def test_portfolio_user_detail_url_is_resolved(self):
        url = reverse('portfolio_detail')
        self.assertEqual(resolve(url).func.view_class, PortfolioUserDetailView)

    def test_portfolio_view_url_is_resolved(self):
        url = reverse('portfolio_view', kwargs={'user_id': 1})
        self.assertEqual(resolve(url).func.view_class, PortfolioDetailView)

    def test_buy_stock_url_is_resolved(self):
        url = reverse('buy_stock')
        self.assertEqual(resolve(url).func.view_class, BuyStock)

    def test_sell_stock_url_is_resolved(self):
        url = reverse('sell_stock')
        self.assertEqual(resolve(url).func.view_class, SellStock)

    def test_stock_price_url_is_resolved(self):
        url = reverse('stock_price', kwargs={'stock_id': '1'})
        self.assertEqual(resolve(url).func.view_class, StockPrice)

    def test_user_orders_url_is_resolved(self):
        url = reverse('user_orders')
        self.assertEqual(resolve(url).func.view_class, UserOrders)

    def test_generate_join_link_url_is_resolved(self):
        url = reverse('generate_join_link', kwargs={'team_id': 1})
        self.assertEqual(resolve(url).func.view_class, GenerateJoinLink)

    def test_update_member_role_url_is_resolved(self):
        url = reverse('update_member_role', kwargs={'team_id': 1, 'user_id': 1})
        self.assertEqual(resolve(url).func.view_class, UpdateMemberRole)

    def test_interact_with_ollama_url_is_resolved(self):
        url = reverse('interact-with-ollama')
        self.assertEqual(resolve(url).func.view_class, InteractWithOllama)

    def test_create_news_ai_url_is_resolved(self):
        url = reverse('create-news-ai')
        self.assertEqual(resolve(url).func.view_class, CreateNewsAI)

    def test_create_event_ai_url_is_resolved(self):
        url = reverse('create-event-ai')
        self.assertEqual(resolve(url).func.view_class, CreateEventAI)

    def test_create_trigger_ai_url_is_resolved(self):
        url = reverse('create-trigger-ai')
        self.assertEqual(resolve(url).func.view_class, CreateTriggerAI)

    def test_create_company_stock_ai_url_is_resolved(self):
        url = reverse('create-company-stock-ai')
        self.assertEqual(resolve(url).func.view_class, CreateCompanyAndStockAI)

    def test_create_scenario_ai_url_is_resolved(self):
        url = reverse('create-scenario-ai')
        self.assertEqual(resolve(url).func.view_class, CreateScenarioAI)

    def test_company_management_create_url_is_resolved(self):
        url = reverse('create_company')
        self.assertEqual(resolve(url).func.view_class, CompanyManagement)

    def test_company_management_manage_url_is_resolved(self):
        url = reverse('manage_company', kwargs={'company_id': 1})
        self.assertEqual(resolve(url).func.view_class, CompanyManagement)

    def test_scenario_management_create_url_is_resolved(self):
        url = reverse('create_scenario')
        self.assertEqual(resolve(url).func.view_class, ScenarioManagement)

    def test_scenario_management_manage_url_is_resolved(self):
        url = reverse('manage_scenario', kwargs={'scenario_id': 1})
        self.assertEqual(resolve(url).func.view_class, ScenarioManagement)

    def test_scenario_manager_management_create_url_is_resolved(self):
        url = reverse('create_scenario_manager')
        self.assertEqual(resolve(url).func.view_class, ScenarioManagerManagement)

    def test_scenario_manager_management_manage_url_is_resolved(self):
        url = reverse('manage_scenario_manager', kwargs={'scenario_manager_id': 1})
        self.assertEqual(resolve(url).func.view_class, ScenarioManagerManagement)

    def test_scenario_manager_stocks_url_is_resolved(self):
        url = reverse('scenario_manager_stocks', kwargs={'scenario_manager_id': 1})
        self.assertEqual(resolve(url).func.view_class, ScenarioManagerStocks)

    def test_scenario_manager_teams_url_is_resolved(self):
        url = reverse('scenario_manager_teams', kwargs={'scenario_manager_id': 1})
        self.assertEqual(resolve(url).func.view_class, ScenarioManagerTeams)

    def test_scenario_manager_events_url_is_resolved(self):
        url = reverse('scenario_manager_events', kwargs={'scenario_manager_id': 1})
        self.assertEqual(resolve(url).func.view_class, ScenarioManagerEvents)

    def test_scenario_manager_triggers_url_is_resolved(self):
        url = reverse('scenario_manager_triggers', kwargs={'scenario_manager_id': 1})
        self.assertEqual(resolve(url).func.view_class, ScenarioManagerTriggers)

    def test_scenario_manager_news_url_is_resolved(self):
        url = reverse('scenario_manager_news', kwargs={'scenario_manager_id': 1})
        self.assertEqual(resolve(url).func.view_class, ScenarioManagerNews)

    def test_change_scenario_manager_state_url_is_resolved(self):
        url = reverse('change_state', kwargs={'scenario_manager_id': 1})
        self.assertEqual(resolve(url).func.view_class, ChangeScenarioManagerState)

    def test_news_management_create_url_is_resolved(self):
        url = reverse('create_news')
        self.assertEqual(resolve(url).func.view_class, NewsManagement)

    def test_news_management_manage_url_is_resolved(self):
        url = reverse('manage_news', kwargs={'news_id': 1})
        self.assertEqual(resolve(url).func.view_class, NewsManagement)

    def test_event_management_create_url_is_resolved(self):
        url = reverse('create_event')
        self.assertEqual(resolve(url).func.view_class, EventManagement)

    def test_event_management_manage_url_is_resolved(self):
        url = reverse('manage_event', kwargs={'event_id': 1})
        self.assertEqual(resolve(url).func.view_class, EventManagement)

    def test_trigger_management_create_url_is_resolved(self):
        url = reverse('create_trigger')
        self.assertEqual(resolve(url).func.view_class, TriggerManagement)

    def test_trigger_management_manage_url_is_resolved(self):
        url = reverse('manage_trigger', kwargs={'trigger_id': 1})
        self.assertEqual(resolve(url).func.view_class, TriggerManagement)

    def test_stock_management_create_url_is_resolved(self):
        url = reverse('create_stock')
        self.assertEqual(resolve(url).func.view_class, StockManagement)

    def test_stock_management_manage_url_is_resolved(self):
        url = reverse('manage_stock', kwargs={'stock_id': 1})
        self.assertEqual(resolve(url).func.view_class, StockManagement)

    def test_stock_price_history_list_url_is_resolved(self):
        url = reverse('price_history_list')
        self.assertEqual(resolve(url).func.view_class, StockPriceHistoryManagement)

    def test_stock_price_history_detail_url_is_resolved(self):
        url = reverse('price_history_detail', kwargs={'price_history_id': 1})
        self.assertEqual(resolve(url).func.view_class, StockPriceHistoryManagement)
