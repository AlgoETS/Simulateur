# simulation/forms.py
from django import forms
from simulation.models import (
    Company, Stock, Team, JoinLink, UserProfile, Event, Trigger, SimulationSettings,
    Scenario, Portfolio, TransactionHistory, SimulationData, Order, News
)

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'backstory']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['company', 'ticker', 'price', 'partial_share', 'complete_share']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'balance', 'members']

class JoinLinkForm(forms.ModelForm):
    class Meta:
        model = JoinLink
        fields = ['team', 'key', 'expires_at']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'balance', 'team']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'impact', 'event_type', 'trigger_date']

class TriggerForm(forms.ModelForm):
    class Meta:
        model = Trigger
        fields = ['name', 'description', 'trigger_type', 'trigger_value', 'event']

class SimulationSettingsForm(forms.ModelForm):
    class Meta:
        model = SimulationSettings
        fields = [
            'max_users', 'max_companies', 'timer_step', 'timer_step_unit', 'interval',
            'interval_unit', 'max_interval', 'fluctuation_rate', 'time_unit', 
            'close_stock_market_at_night', 'noise_function'
        ]

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            'name', 'description', 'backstory', 'duration', 
            'companies', 'stocks', 'users', 'teams', 'events', 'triggers', 'simulation_settings'
        ]
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'impact', 'event']
