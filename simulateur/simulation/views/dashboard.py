# simulation/views.py
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

from simulation.models import (
    SimulationSettings, UserProfile, Stock, Cryptocurrency, Event, Portfolio, TransactionHistory,
    Trigger, News, Company, Team, JoinLink, Scenario, SimulationData, Order
)
from simulation.forms import (
    EventForm, TriggerForm, NewsForm, CompanyForm, StockForm, TeamForm, JoinLinkForm, UserProfileForm,
    SimulationSettingsForm, ScenarioForm, PortfolioForm, TransactionHistoryForm, SimulationDataForm, OrderForm
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
        cryptos = Cryptocurrency.objects.all()
        context = {
            'portfolio': user_profile.portfolio,
            'transactions': transactions,
            'stocks': stocks,
            'cryptos': cryptos
        }
        return render(request, 'simulation/user_dashboard.html', context)

class AdminDashboardView(AdminOnlyMixin, View):
    def get(self, request):
        portfolios = Portfolio.objects.all()
        settings = SimulationSettings.objects.first()
        context = {
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
            'team': team,
            'portfolios': portfolios
        }
        return render(request, 'simulation/team_dashboard.html', context)

class MarketOverviewView(View):
    def get(self, request):
        stocks = Stock.objects.all()
        cryptos = Cryptocurrency.objects.all()
        events = Event.objects.all()
        context = {
            'stocks': stocks,
            'cryptos': cryptos,
            'events': events
        }
        return render(request, 'simulation/market_overview.html', context)

class BuySellView(View):
    def get(self, request, stock_id):
        stock = Stock.objects.get(id=stock_id)
        context = {
            'stock': stock
        }
        return render(request, 'simulation/buy_sell.html', context)

class CreateEventView(AdminOnlyMixin, View):
    def get(self, request):
        form = EventForm()
        return render(request, 'simulation/create_event.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('admin_dashboard')
        return render(request, 'simulation/create_event.html', {'form': form})

class CreateTriggerView(AdminOnlyMixin, View):
    def get(self, request):
        form = TriggerForm()
        return render(request, 'simulation/create_trigger.html', {'form': form})

    def post(self, request):
        form = TriggerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trigger created successfully.')
            return redirect('admin_dashboard')
        return render(request, 'simulation/create_trigger.html', {'form': form})

class CreateNewsView(AdminOnlyMixin, View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'simulation/create_news.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'News created successfully.')
            return redirect('admin_dashboard')
        return render(request, 'simulation/create_news.html', {'form': form})

class CreateCompanyView(AdminOnlyMixin, View):
    def get(self, request):
        form = CompanyForm()
        return render(request, 'simulation/create_company.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created successfully.')
            return redirect('admin_dashboard')
        return render(request, 'simulation/create_company.html', {'form': form})

class CreateStockView(AdminOnlyMixin, View):
    def get(self, request):
        form = StockForm()
        return render(request, 'simulation/create_stock.html', {'form': form})

    def post(self, request):
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock created successfully.')
            return redirect('admin_dashboard')
        return render(request, 'simulation/create_stock.html', {'form': form})

class SimulationSettingsView(AdminOnlyMixin, View):
    def get(self, request):
        settings = SimulationSettings.objects.first()
        form = SimulationSettingsForm(instance=settings)
        return render(request, 'simulation/settings.html', {'form': form})

    def post(self, request):
        settings = SimulationSettings.objects.first()
        form = SimulationSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('admin_dashboard')
        return render(request, 'simulation/settings.html', {'form': form})

class CreateScenarioView(AdminOnlyMixin, View):
    def get(self, request):
        form = ScenarioForm()
        return render(request, 'simulation/create_scenario.html', {'form': form})

    def post(self, request):
        form = ScenarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scenario created successfully.')
            return redirect('admin_dashboard')
        return render(request, 'simulation/create_scenario.html', {'form': form})
