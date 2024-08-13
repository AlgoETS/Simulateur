from django.test import SimpleTestCase
from django.urls import reverse, resolve
from simulation.api.auth import UpdateMemberRole
from simulation.api.portfolio import (
    BuyStock,
    SellStock,
    StockPrice,
)
from simulation.api.teams import GenerateJoinLink
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

from simulation.api.transaction import UserOrders


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
