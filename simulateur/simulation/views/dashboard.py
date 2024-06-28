from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

from simulation.models import (
    SimulationSettings,
    UserProfile,
    Stock,
    Event,
    Portfolio,
    TransactionHistory,
    Trigger,
    News,
    Company,
    Team,
    JoinLink,
    Scenario,
    SimulationData,
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

        transactions = TransactionHistory.objects.filter(
            portfolio=user_profile.portfolio
        )
        stocks = Stock.objects.all()
        context = {
            "title": "User Dashboard",
            "portfolio": user_profile.portfolio,
            "transactions": transactions,
            "stocks": stocks,
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
        user_profile = UserProfile.objects.get(user=request.user)
        team = user_profile.team
        portfolios = Portfolio.objects.filter(team=team)
        context = {"title": "Team Dashboard", "team": team, "portfolios": portfolios}
        return render(request, "dashboard/team_dashboard.html", context)

class GameDashboardView(View):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        team = user_profile.team
        portfolios = Portfolio.objects.filter(team=team)
        companies = Company.objects.all()
        stock = Stock.objects.all()
        transactions = TransactionHistory.objects.filter(portfolio__in=portfolios)
        news_items = News.objects.all()

        # Prepare company data for charts
        companies_data = []
        for company in companies:
            stock_prices = company.stock_set.all().order_by('timestamp').values('timestamp', 'price', 'open_price', 'high_price', 'low_price', 'close_price')
            # convert timestamp to string
            stock_prices = map(lambda x: {**x, 'timestamp': x['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}, stock_prices)
            companies_data.append({
                'id': company.id,
                'name': company.name,
                'ticker': stock.get(company=company).ticker,
                'stock_prices': list(stock_prices)
            })

        context = {
            'title': 'Game Dashboard',
            'team': team,
            'portfolios': portfolios,
            'transactions': transactions,
            'companies': companies_data,
            'news_items': news_items
        }
        return render(request, 'dashboard/game_dashboard.html', context)

class MarketOverviewView(View):
    def get(self, request):
        stocks = Stock.objects.all()
        events = Event.objects.all()
        context = {"title": "Market Overview", "stocks": stocks, "events": events}
        return render(request, "simulation/market_overview.html", context)

class BuySellView(View):
    def get(self, request, stock_id):
        stock = Stock.objects.get(id=stock_id)
        context = {"title": "Buy/Sell", "stock": stock}
        return render(request, "simulation/buy_sell.html", context)
