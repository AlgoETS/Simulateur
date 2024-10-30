from rest_framework import serializers
from .models import (
    Company, Stock, UserProfile, Event, SimulationSettings,
    Scenario, Team, Portfolio, TransactionHistory, Trigger, News, StockPriceHistory, Simulation
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'backstory', 'sector', 'country', 'industry']


class StockPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPriceHistory
        fields = ['open_price', 'high_price', 'low_price', 'close_price', 'timestamp']


class StockSerializer(serializers.ModelSerializer):
    price_history = StockPriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'company', 'ticker', 'volatility', 'liquidity', 'price_history']

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        company, created = Company.objects.get_or_create(**company_data)
        stock = Stock.objects.create(company=company, **validated_data)
        return stock


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
        fields = ['title', 'content', 'published_date']


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = [
            'id', 'name', 'description', 'backstory', 'duration',
        ]

class SimulationManagerSerializer(serializers.ModelSerializer):
    scenario = ScenarioSerializer()
    stocks = StockSerializer(many=True)
    teams = TeamSerializer(many=True)
    events = EventSerializer(many=True)
    triggers = TriggerSerializer(many=True)
    news = NewsSerializer(many=True)
    simulation_settings = SimulationSettingsSerializer()

    class Meta:
        model = Simulation
        fields = [
            'scenario', 'stocks', 'teams', 'events', 'triggers', 'news',
            'simulation_settings', 'state', 'timestamp', 'published_date'
        ]


class JoinTeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    key = serializers.CharField(max_length=32)


class UpdateTeamNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class UpdateMemberRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=[
        ('member', 'Member'),
        ('team_leader', 'Team Leader'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
        ('moderator', 'Moderator')
    ])


class RemoveMemberSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()
