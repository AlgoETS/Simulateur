from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
import json

from simulation.models import (
    UserProfile,
    Stock,
    Portfolio,
    TransactionHistory,
    StockPortfolio,
    Team,
    News,
    Company,
    Event,
    SimulationSettings,
    Scenario,
    Order,
    Trigger,
)
import logging

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)  # 15 minutes default

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
        try:
            user_profile = UserProfile.objects.select_related('user').get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile does not exist. Please create your profile.")
            return redirect(reverse("home"))
        except Exception as e:
            messages.error(request, str(e))
            logger.error(f"Unexpected error: {e}")
            return redirect(reverse("home"))

        # Ensure the user has a portfolio
        portfolio, created = Portfolio.objects.get_or_create(owner=user_profile)
        if created:
            user_profile.portfolio = portfolio
            user_profile.save()

        # Get the selected scenario
        scenarios = Scenario.objects.all()
        current_scenario_id = request.GET.get('scenario', scenarios.first().id if scenarios.exists() else None)

        # Fetch necessary data
        orders = Order.objects.filter(user=user_profile, scenario_id=current_scenario_id).select_related('stock').order_by("-timestamp")
        stocks = Stock.objects.filter(scenarios_stocks__id=current_scenario_id).select_related('company')

        # Get the user's portfolio
        portfolio = user_profile.portfolio
        stocks_data = StockPortfolio.objects.filter(portfolio=portfolio, stock__in=stocks)

        # Get the user's balance
        balance = portfolio.balance

        # Get the user's total stock value
        total_stock_value = stocks_data.aggregate(
            total_stock_value=Sum('stock__price') * Sum('quantity')
        )['total_stock_value']

        context = {
            "title": "User Dashboard",
            "user_profile": user_profile,
            "portfolio": portfolio,
            "stocks": stocks,
            "orders": orders,
            "scenarios": scenarios,
            "current_scenario_id": current_scenario_id,
            "stocks_data": stocks_data,
            "balance": balance,
            "total_stock_value": total_stock_value,
        }

        return render(request, "dashboard/user_dashboard.html", context)

class AdminDashboardView(AdminOnlyMixin, View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        scenarios = Scenario.objects.all()
        news = News.objects.all()
        events = Event.objects.all()
        triggers = Trigger.objects.all()
        companies = Company.objects.all()
        stocks = Stock.objects.all()

        context = {
            "title": "Admin Dashboard",
            "scenarios": scenarios,
            "news": news,
            "events": events,
            "triggers": triggers,
            "companies": companies,
            "stocks": stocks,
        }
        return render(request, "dashboard/admin_dashboard.html", context)

class TeamDashboardView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        try:
            user_profile = UserProfile.objects.select_related('user').get(user=request.user)
            team = user_profile.team
            if not team:
                messages.error(request, "You are not part of any team. Please join a team.")
                return redirect(reverse("join_team"))

            portfolios = Portfolio.objects.filter(owner__team=team)
            members = team.user_profiles.all()

            context = {
                "title": "Team Dashboard",
                "team": team,
                "portfolios": portfolios,
                "members": members,
            }
            return render(request, "dashboard/team_dashboard.html", context)
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile does not exist. Please create your profile.")
            return redirect(reverse("home"))
        except Team.DoesNotExist:
            messages.error(request, "Team does not exist.")
            return redirect(reverse("home"))
        except Exception as e:
            messages.error(request, str(e))
            return redirect(reverse("home"))

class GameDashboardView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile does not exist. Please create your profile.")
            return redirect(reverse("signup"))
        except Exception as e:
            messages.error(request, str(e))
            return redirect(reverse("home"))

        team = user_profile.team
        user_profiles_in_team = UserProfile.objects.filter(team=team)
        portfolios = Portfolio.objects.filter(owner__in=user_profiles_in_team)
        stocks = Stock.objects.all()
        transactions = TransactionHistory.objects.filter(portfolios__in=portfolios)
        news_items = News.objects.all()
        scenarios = Scenario.objects.all()

        stocks_data = []
        for stock in stocks:
            stock_prices = stock.price_history.order_by("timestamp").values(
                "timestamp", "open_price", "high_price", "low_price", "close_price"
            )
            stock_prices = list(map(lambda x: {**x, "timestamp": x["timestamp"].strftime("%Y-%m-%d %H:%M:%S")}, stock_prices))
            stocks_data.append({
                "id": stock.id,
                "name": stock.company.name,
                "ticker": stock.ticker,
                "stock_prices": stock_prices,
            })

        context = {
            "title": "Game Dashboard",
            "team": team,
            "portfolios": portfolios,
            "transactions": transactions,
            "stocks": stocks_data,
            "news_items": news_items,
            "scenarios": scenarios,
        }

        # Set client-side cache headers
        response = render(request, "dashboard/game_dashboard.html", context)
        response['Cache-Control'] = f'public, max-age={CACHE_TTL}'
        return response

class MarketOverviewView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        stocks = Stock.objects.select_related('company').all()
        events = Event.objects.all()
        companies = Company.objects.all()
        news_items = News.objects.all().order_by('-published_date')[:5]
        transactions = TransactionHistory.objects.prefetch_related('orders').all()
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
        transactions = TransactionHistory.objects.filter(portfolios=portfolio).order_by(
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
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(
                request, "User profile does not exist. Please create your profile."
            )
            return redirect(reverse("create_user_profile"))
        except Exception as e:
            messages.error(request, str(e))
            return redirect(reverse("home"))

        if not hasattr(user_profile, "portfolio"):
            portfolio = Portfolio.objects.create(owner=user_profile)
            user_profile.portfolio = portfolio
            user_profile.save()

        portfolio = user_profile.portfolio
        transactions = TransactionHistory.objects.filter(portfolios=portfolio).order_by(
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
