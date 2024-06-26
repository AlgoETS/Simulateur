# simulation/views.py
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

from simulation.models import (
    SimulationSettings, UserProfile, Stock, Event, Portfolio, TransactionHistory,
    Trigger, News, Company, Team, JoinLink, Scenario, SimulationData, Order
)
from simulation.forms import (
    EventForm, TriggerForm, NewsForm, CompanyForm, StockForm, TeamForm, JoinLinkForm, UserProfileForm,
    SimulationSettingsForm, ScenarioForm, PortfolioForm, TransactionHistoryForm, OrderForm
)

class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class HomeView(View):
    def get(self, request):
        return render(request, 'simulation/home.html')

class UserDashboardView(View):
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile does not exist. Please create your profile.")
            return redirect(reverse('create_user_profile'))

        transactions = TransactionHistory.objects.filter(portfolio=user_profile.portfolio)
        stocks = Stock.objects.all()
        context = {
            'title': 'User Dashboard',
            'portfolio': user_profile.portfolio,
            'transactions': transactions,
            'stocks': stocks,
        }
        return render(request, 'simulation/user_dashboard.html', context)

class AdminDashboardView(AdminOnlyMixin, View):
    def get(self, request):
        portfolios = Portfolio.objects.all()
        settings = SimulationSettings.objects.first()
        context = {
            'title': 'Admin Dashboard',
            'portfolios': portfolios,
            'settings': settings
        }
        return render(request, 'simulation/admin_dashboard.html', context)

class TeamDashboardView(View):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        team = user_profile.team
        portfolios = Portfolio.objects.filter(team=team)
        context = {
            'title': 'Team Dashboard',
            'team': team,
            'portfolios': portfolios
        }
        return render(request, 'simulation/team_dashboard.html', context)

class MarketOverviewView(View):
    def get(self, request):
        stocks = Stock.objects.all()
        events = Event.objects.all()
        context = {
            'title': 'Market Overview',
            'stocks': stocks,
            'events': events
        }
        return render(request, 'simulation/market_overview.html', context)

class BuySellView(View):
    def get(self, request, stock_id):
        stock = Stock.objects.get(id=stock_id)
        context = {
            'title': 'Buy/Sell',
            'stock': stock
        }
        return render(request, 'simulation/buy_sell.html', context)
