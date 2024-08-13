from django.contrib import admin

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
    StockPortfolio,
    News,
    Order,
    JoinLink,
    StockPriceHistory
)

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
admin.site.register(StockPortfolio)
admin.site.register(News)
admin.site.register(Order)
admin.site.register(JoinLink)
admin.site.register(StockPriceHistory)
