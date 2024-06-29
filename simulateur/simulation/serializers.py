from rest_framework import serializers
from .models import (
    Company, SimulationData, Stock, UserProfile, Event, SimulationSettings,
<<<<<<< HEAD
    Scenario, Team, Portfolio, TransactionHistory, Trigger, News, StockPriceHistory
=======
    Scenario, Team, Portfolio, TransactionHistory, Trigger, News
>>>>>>> origin/main
)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'sector', 'industry']

class StockPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPriceHistory
        fields = ['open_price', 'high_price', 'low_price', 'close_price', 'timestamp']

class StockSerializer(serializers.ModelSerializer):
    price_history = StockPriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'company', 'ticker', 'price', 'open_price', 'high_price', 'low_price', 'close_price', 'price_history']

<<<<<<< HEAD
    def create(self, validated_data):
        company_data = validated_data.pop('company')
        company, created = Company.objects.get_or_create(**company_data)
        return Stock.objects.create(company=company, **validated_data)

=======
>>>>>>> origin/main
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'date', 'description']

class SimulationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationSettings
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'

class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        fields = ['name', 'type', 'value', 'timestamp']

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
<<<<<<< HEAD
        fields = ['title', 'content', 'published_date']
=======
        fields = '__all__'
>>>>>>> origin/main

class ScenarioSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    triggers = TriggerSerializer(many=True)
<<<<<<< HEAD
    news = NewsSerializer(many=True)
    teams = TeamSerializer(many=True)
    stocks = StockSerializer(many=True)
    simulation_settings = SimulationSettingsSerializer()
=======
>>>>>>> origin/main

    class Meta:
        model = Scenario
        fields = ['id', 'name', 'description', 'backstory', 'duration', 'stocks', 'users', 'teams', 'news', 'events', 'triggers', 'simulation_settings', 'timestamp', 'published_date']

    def create(self, validated_data):
        events_data = validated_data.pop('events')
        triggers_data = validated_data.pop('triggers')
        news_data = validated_data.pop('news_set')
        teams_data = validated_data.pop('teams')
        stocks_data = validated_data.pop('stocks')

        scenario = Scenario.objects.create(**validated_data)

        for event_data in events_data:
            Event.objects.create(scenario=scenario, **event_data)

        for trigger_data in triggers_data:
            Trigger.objects.create(scenario=scenario, **trigger_data)

        for news_item_data in news_data:
            News.objects.create(scenario=scenario, **news_item_data)

        for team_data in teams_data:
            Team.objects.create(scenario=scenario, **team_data)

        for stock_data in stocks_data:
            stock_serializer = StockSerializer(data=stock_data)
            if stock_serializer.is_valid():
                stock_serializer.save()

        return scenario

class SimulationDataSerializer(serializers.ModelSerializer):
    scenario = ScenarioSerializer()
    portfolio = PortfolioSerializer()
    transactions = TransactionHistorySerializer(many=True)

    class Meta:
        model = SimulationData
        fields = '__all__'

class JoinTeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    key = serializers.CharField(max_length=32)