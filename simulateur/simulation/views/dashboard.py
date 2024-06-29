from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum
from django.db import transaction

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
)


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class HomeView(View):
    def get(self, request):
        return render(request, "simulation/home.html")


class UserDashboardView(View):
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(
                request, "User profile does not exist. Please create your profile."
            )
            return redirect(reverse("create_user_profile"))

        if not hasattr(user_profile, "portfolio"):
            portfolio = Portfolio.objects.create(owner=user_profile)
            user_profile.portfolio = portfolio
            user_profile.save()

        portfolio = user_profile.portfolio
        orders = Order.objects.filter(user=user_profile).order_by("-timestamp")
        stocks = Stock.objects.all()
        scenarios = Scenario.objects.all()
        current_scenario_id = scenarios.first().id if scenarios.exists() else None

        stocks_data = [
            {
                "stock": stock,
                "quantity": StockPortfolio.objects.filter(
                    portfolio=portfolio, stock=stock
                ).aggregate(Sum("quantity"))["quantity__sum"]
                or 0,
            }
            for stock in portfolio.stocks.all()
        ]

        context = {
            "title": "User Dashboard",
            "portfolio": portfolio,
            "orders": orders,
            "stocks": stocks,
            "stocks_data": stocks_data,
            "scenarios": scenarios,
            "current_scenario_id": current_scenario_id,
        }
        return render(request, "dashboard/user_dashboard.html", context)


class AdminDashboardView(AdminOnlyMixin, View):
    def get(self, request):
        portfolios = Portfolio.objects.all()
        settings = SimulationSettings.objects.first()
        context = {
            "title": "Admin Dashboard",
            "portfolios": portfolios,
            "settings": settings,
        }
        return render(request, "dashboard/admin_dashboard.html", context)


class TeamDashboardView(View):
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            team = user_profile.team
            if not team:
                return JsonResponse(
                    {"status": "error", "message": "User is not part of any team"},
                    status=400,
                )

            portfolios = Portfolio.objects.filter(team=team)
            members = team.user_profiles.all()

            context = {
                "title": "Team Dashboard",
                "team": team,
                "portfolios": portfolios,
                "members": members,
            }
            return render(request, "dashboard/team_dashboard.html", context)
        except UserProfile.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "User profile does not exist"},
                status=400,
            )
        except Team.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Team does not exist"}, status=400
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


class GameDashboardView(View):
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return render(
                request,
                "dashboard/game_dashboard.html",
                {"title": "Game Dashboard", "error": "User profile not found."},
            )

        team = user_profile.team
        portfolios = Portfolio.objects.filter(team=team)
        companies = Company.objects.all()
        transactions = TransactionHistory.objects.filter(portfolio__in=portfolios)
        news_items = News.objects.all()

        companies_data = []
        for company in companies:
            if stock := company.stock_set.first():
                stock_prices = (
                    stock.price_history.all()
                    .order_by("timestamp")
                    .values(
                        "timestamp",
                        "price",
                        "open_price",
                        "high_price",
                        "low_price",
                        "close_price",
                    )
                )
                stock_prices = map(
                    lambda x: {
                        **x,
                        "timestamp": x["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    },
                    stock_prices,
                )
                companies_data.append(
                    {
                        "id": company.id,
                        "name": company.name,
                        "ticker": stock.ticker,
                        "stock_prices": list(stock_prices),
                    }
                )

        context = {
            "title": "Game Dashboard",
            "team": team,
            "portfolios": portfolios,
            "transactions": transactions,
            "companies": companies_data,
            "news_items": news_items,
        }
        return render(request, "dashboard/game_dashboard.html", context)


class MarketOverviewView(View):
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
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(
                request, "User profile does not exist. Please create your profile."
            )
            return redirect(reverse("create_user_profile"))

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
