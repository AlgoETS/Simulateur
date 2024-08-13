from django import forms
from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget

from .models import (
    Company,
    Stock,
    UserProfile,
    Event,
    Team,
    SimulationSettings,
    Scenario,
    Portfolio,
    TransactionHistory,
    Trigger,
    SimulationData,
    StockPortfolio,
    News,
    Order,
    JoinLink,
    StockPriceHistory
)


class SimulationDataAdminForm(forms.ModelForm):
    class Meta:
        model = SimulationData
        fields = '__all__'
        widgets = {
            'price_changes': JSONEditorWidget(attrs={'style': 'width: auto; height: 500px;'}),
            'transactions': JSONEditorWidget(attrs={'style': 'width: auto; height: 500px;'}),
        }


class SimulationDataAdmin(admin.ModelAdmin):
    form = SimulationDataAdminForm


admin.site.register(Company)
admin.site.register(Stock)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(SimulationSettings)
admin.site.register(Scenario)
admin.site.register(Portfolio)
admin.site.register(TransactionHistory)
admin.site.register(Trigger)
admin.site.register(SimulationData, SimulationDataAdmin)
admin.site.register(StockPortfolio)
admin.site.register(News)
admin.site.register(Order)
admin.site.register(JoinLink)
admin.site.register(StockPriceHistory)
