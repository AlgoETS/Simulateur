import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum, F, Subquery, OuterRef
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from simulation.models import (
    UserProfile, Stock, Portfolio, TransactionHistory, StockPortfolio, Team,
    News, Company, Event, SimulationManager, Trigger, StockPriceHistory
)

logger = logging.getLogger(__name__)
CACHE_TTL = getattr(settings, 'CACHE_TTL', 30)  # 30 seconds

# Utility functions
def get_user_profile(request):
    try:
        return UserProfile.objects.select_related('user').get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile does not exist. Please create your profile.")
        return None
    except Exception as e:
        messages.error(request, str(e))
        return None


def get_or_create_portfolio(user_profile, simulation_manager):
    portfolio, created = Portfolio.objects.get_or_create(
        owner=user_profile,
        simulation_manager=simulation_manager
    )
    if created:
        user_profile.portfolio = portfolio
        user_profile.save()
    return portfolio


def get_current_simulation_manager(simulation_managers, request):
    current_simulation_manager_id = request.GET.get('simulation_manager', simulation_managers.first().id if simulation_managers.exists() else None)
    if not current_simulation_manager_id:
        messages.error(request, "No simulation managers available.")
        return None, None
    try:
        current_simulation_manager = simulation_managers.get(id=current_simulation_manager_id)
        return current_simulation_manager_id, current_simulation_manager
    except SimulationManager.DoesNotExist:
        return None, None


def get_transactions(simulation_manager):
    transactions, _ = TransactionHistory.objects.get_or_create(simulation_manager=simulation_manager)
    orders = transactions.orders.all()
    return transactions, orders


def get_portfolio_data(portfolio, simulation_manager):
    stocks = Stock.objects.filter(scenarios_stocks__id=simulation_manager.id).select_related('company')

    latest_price = StockPriceHistory.objects.filter(
        stock=OuterRef('stock_id')
    ).order_by('-timestamp').values('close_price')[:1]

    stocks_data = StockPortfolio.objects.filter(
        portfolio=portfolio, stock__in=stocks
    ).annotate(
        current_price=Subquery(latest_price)
    )

    balance = portfolio.balance
    total_stock_value = stocks_data.aggregate(
        total_stock_value=Sum(F('current_price') * F('quantity'))
    )['total_stock_value'] or 0

    return stocks, stocks_data, total_stock_value, balance


def get_price_history(stocks_data):
    stock_ids = [stock_data.stock.id for stock_data in stocks_data]
    return StockPriceHistory.objects.filter(
        stock__in=stock_ids
    ).order_by('timestamp')


def get_user_team(user_profile):
    return Team.objects.filter(members=user_profile).first()


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class HomeView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        return render(request, "simulation/home.html")


class UserDashboardView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        user_profile = get_user_profile(request)
        if not user_profile:
            return redirect(reverse("home"))

        simulation_managers = SimulationManager.objects.all()
        current_simulation_manager_id, current_simulation_manager = get_current_simulation_manager(simulation_managers, request)

        if not current_simulation_manager:
            messages.error(request, "Selected simulation manager does not exist.")
            return redirect(reverse("home"))

        portfolio = get_or_create_portfolio(user_profile, current_simulation_manager)
        transactions, orders = get_transactions(current_simulation_manager)
        stocks, stocks_data, total_stock_value, balance = get_portfolio_data(portfolio, current_simulation_manager)
        price_history = get_price_history(stocks_data)

        context = {
            "title": "User Dashboard",
            "user_profile": user_profile,
            "portfolio": portfolio,
            "stocks": stocks,
            "orders": orders,
            "simulation_managers": simulation_managers,
            "current_simulation_manager_id": current_simulation_manager_id,
            "stocks_data": stocks_data,
            "balance": balance,
            "total_stock_value": total_stock_value,
            "price_history": price_history,
        }

        return render(request, "dashboard/user_dashboard.html", context)


class AdminDashboardView(AdminOnlyMixin, View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        simulation_managers = SimulationManager.objects.all()
        news = News.objects.all()
        events = Event.objects.all()
        triggers = Trigger.objects.all()
        companies = Company.objects.all()
        stocks = Stock.objects.all()

        context = {
            "title": "Admin Dashboard",
            "simulation_managers": simulation_managers,
            "news": news,
            "events": events,
            "triggers": triggers,
            "companies": companies,
            "stocks": stocks,
        }
        return render(request, "dashboard/admin_dashboard.html", context)


class TeamDashboardView(View):
    def get(self, request):
        user_profile = get_user_profile(request)
        if not user_profile:
            return redirect(reverse("home"))

        team = get_user_team(user_profile)
        if not team:
            messages.error(request, "You are not part of any team. Please join or create a team.")
            return redirect(reverse("join_team"))

        portfolios = Portfolio.objects.filter(owner__team=team)
        members = team.members.all()

        context = {
            "title": "Team Dashboard",
            "team": team,
            "portfolios": portfolios,
            "members": members,
            "team_balance": sum(portfolio.balance for portfolio in portfolios),
        }
        return render(request, "dashboard/team_dashboard.html", context)


class GameDashboardView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        user_profile = get_user_profile(request)
        if not user_profile:
            return redirect(reverse("home"))

        team = get_user_team(user_profile)
        if not team:
            messages.error(request, "You are not part of any team. Please join or create a team.")
            return redirect(reverse("join_team"))

        context = self.get_dashboard_context(team)
        response = render(request, "dashboard/game_dashboard.html", context)
        response['Cache-Control'] = f'public, max-age={CACHE_TTL}'
        return response

    def get_dashboard_context(self, team):
        user_profiles_in_team = team.members.all()
        portfolios = Portfolio.objects.filter(owner__in=user_profiles_in_team)
        simulation_managers = portfolios.values_list('simulation_manager', flat=True)
        transactions = TransactionHistory.objects.filter(simulation_manager__in=simulation_managers)
        news_items = News.objects.all()

        stocks = Stock.objects.all()
        stocks_data = self.get_stocks_data(stocks)

        return {
            "title": "Game Dashboard",
            "team": team,
            "portfolios": portfolios,
            "transactions": transactions,
            "stocks": stocks_data,
            "news_items": news_items,
            "simulation_managers": SimulationManager.objects.all(),
        }

    def get_stocks_data(self, stocks):
        stocks_data = []
        for stock in stocks:
            stock_prices = stock.price_history.order_by("timestamp").values(
                "timestamp", "open_price", "high_price", "low_price", "close_price"
            )
            stock_prices = [
                {**x, "timestamp": x["timestamp"].strftime("%Y-%m-%d %H:%M:%S")} for x in stock_prices
            ]
            stocks_data.append({
                "id": stock.id,
                "name": stock.company.name,
                "ticker": stock.ticker,
                "stock_prices": stock_prices,
            })
        return stocks_data


class MarketOverviewView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        stocks = Stock.objects.select_related('company').all()
        events = Event.objects.all()
        companies = Company.objects.all()
        news_items = News.objects.all().order_by('-published_date')[:5]
        transactions = TransactionHistory.objects.all()
        teams = Team.objects.all()

        context = {
            "title": "Market Overview",
            "stocks": stocks,
            "events": events,
            "companies": companies,
            "news_items": news_items,
            "transactions": transactions,
            "teams": teams,
        }
        return render(request, "simulation/market_overview.html", context)


class PortfolioDetailView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, portfolio_id):
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        simulation_manager = portfolio.simulation_manager
        transactions = TransactionHistory.objects.filter(simulation_manager=simulation_manager).order_by(
            "-orders__timestamp"
        )
        stocks_data = StockPortfolio.objects.filter(portfolio=portfolio)
        context = {
            "title": "Portfolio Detail",
            "portfolio": portfolio,
            "transactions": transactions,
            "stocks_data": stocks_data,
        }
        return render(request, "portfolio/portfolio_detail.html", context)


class PortfolioUserDetailView(View):
    def get(self, request):
        user_profile = get_user_profile(request)
        if not user_profile:
            return redirect(reverse("create_user_profile"))

        portfolio = get_or_create_portfolio(user_profile, simulation_manager=user_profile.portfolio.simulation_manager)
        transactions = TransactionHistory.objects.filter(simulation_manager=portfolio.simulation_manager).order_by(
            "-orders__timestamp"
        )
        stocks_data = StockPortfolio.objects.filter(portfolio=portfolio)
        context = {
            "title": "Portfolio Detail",
            "portfolio": portfolio,
            "transactions": transactions,
            "stocks_data": stocks_data,
        }
        return render(request, "portfolio/portfolio_detail.html", context)
