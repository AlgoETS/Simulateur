from datetime import timezone

from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from simulation.models import ScenarioManager, Scenario, Stock, Team, Event, Trigger, News, SimulationSettings
from simulation.serializers import SimulationSettingsSerializer


class ScenarioManagerManagement(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data

        scenario_id = data.get('scenario_id')
        if not scenario_id:
            return Response(
                {'status': 'error', 'message': 'Scenario ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        scenario = get_object_or_404(Scenario, id=scenario_id)

        # Create related entities
        stock_ids = data.get('stocks', [])
        team_ids = data.get('teams', [])
        event_ids = data.get('events', [])
        trigger_ids = data.get('triggers', [])
        news_ids = data.get('news', [])
        simulation_settings_data = data.get('simulation_settings')

        # Link stocks
        stocks = Stock.objects.filter(id__in=stock_ids)
        teams = Team.objects.filter(id__in=team_ids)
        events = Event.objects.filter(id__in=event_ids)
        triggers = Trigger.objects.filter(id__in=trigger_ids)
        news = News.objects.filter(id__in=news_ids)

        # Create SimulationSettings if provided
        simulation_settings = SimulationSettings.objects.create(**simulation_settings_data) if simulation_settings_data else None

        scenario_manager = ScenarioManager.objects.create(
            scenario=scenario,
            simulation_settings=simulation_settings,
            state=data.get('state', ScenarioManager.ScenarioState.INITIALIZED)
        )

        scenario_manager.stocks.set(stocks)
        scenario_manager.teams.set(teams)
        scenario_manager.events.set(events)
        scenario_manager.triggers.set(triggers)
        scenario_manager.news.set(news)

        return Response(
            {
                'status': 'success',
                'message': 'ScenarioManager created successfully',
                'data': self.serialize_scenario_manager(scenario_manager)
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request, scenario_manager_id=None, *args, **kwargs):
        if scenario_manager_id:
            scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
            return Response(
                {'status': 'success', 'data': self.serialize_scenario_manager(scenario_manager)},
                status=status.HTTP_200_OK
            )
        else:
            scenario_managers = ScenarioManager.objects.all()
            data = [self.serialize_scenario_manager(sm) for sm in scenario_managers]
            return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)

    def put(self, request, scenario_manager_id, *args, **kwargs):
        scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
        data = request.data

        # Update linked entities and state if provided
        stock_ids = data.get('stocks', [])
        team_ids = data.get('teams', [])
        event_ids = data.get('events', [])
        trigger_ids = data.get('triggers', [])
        news_ids = data.get('news', [])
        simulation_settings_data = data.get('simulation_settings')

        # Link stocks
        stocks = Stock.objects.filter(id__in=stock_ids)
        scenario_manager.stocks.set(stocks)

        # Link teams
        teams = Team.objects.filter(id__in=team_ids)
        scenario_manager.teams.set(teams)

        # Link events
        events = Event.objects.filter(id__in=event_ids)
        scenario_manager.events.set(events)

        # Link triggers
        triggers = Trigger.objects.filter(id__in=trigger_ids)
        scenario_manager.triggers.set(triggers)

        # Link news
        news = News.objects.filter(id__in=news_ids)
        scenario_manager.news.set(news)

        # Update SimulationSettings if provided
        if simulation_settings_data and scenario_manager.simulation_settings:
            for key, value in simulation_settings_data.items():
                setattr(scenario_manager.simulation_settings, key, value)
            scenario_manager.simulation_settings.save()

        # Update state
        scenario_manager.state = data.get('state', scenario_manager.state)
        scenario_manager.save()

        return Response(
            {
                'status': 'success',
                'message': 'ScenarioManager updated successfully',
                'data': self.serialize_scenario_manager(scenario_manager)
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, scenario_manager_id, *args, **kwargs):
        scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
        scenario_manager.delete()
        return Response(
            {'status': 'success', 'message': 'ScenarioManager deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def serialize_scenario_manager(self, scenario_manager):
        return {
            'id': scenario_manager.id,
            'scenario': scenario_manager.scenario.name,
            'state': scenario_manager.state,
            'stocks': [stock.ticker for stock in scenario_manager.stocks.all()],
            'teams': [team.name for team in scenario_manager.teams.all()],
            'events': [event.name for event in scenario_manager.events.all()],
            'triggers': [trigger.name for trigger in scenario_manager.triggers.all()],
            'news': [news_item.title for news_item in scenario_manager.news.all()],
            'simulation_settings': SimulationSettingsSerializer(scenario_manager.simulation_settings).data if scenario_manager.simulation_settings else None,
            'timestamp': scenario_manager.timestamp,
            'published_date': scenario_manager.published_date
        }

class ScenarioManagerStocks(APIView):
    def get(self, request, scenario_manager_id, *args, **kwargs):
        scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
        stocks = scenario_manager.stocks.all()
        stock_data = [{'id': stock.id, 'ticker': stock.ticker} for stock in stocks]
        return Response({'status': 'success', 'data': stock_data}, status=status.HTTP_200_OK)

class ScenarioManagerTeams(APIView):
    def get(self, request, scenario_manager_id, *args, **kwargs):
        scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
        teams = scenario_manager.teams.all()
        team_data = [{'id': team.id, 'name': team.name} for team in teams]
        return Response({'status': 'success', 'data': team_data}, status=status.HTTP_200_OK)

class ScenarioManagerEvents(APIView):
    def get(self, request, scenario_manager_id, *args, **kwargs):
        scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
        events = scenario_manager.events.all()
        event_data = [{'id': event.id, 'name': event.name} for event in events]
        return Response({'status': 'success', 'data': event_data}, status=status.HTTP_200_OK)

class ScenarioManagerTriggers(APIView):
    def get(self, request, scenario_manager_id, *args, **kwargs):
        scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
        triggers = scenario_manager.triggers.all()
        trigger_data = [{'id': trigger.id, 'name': trigger.name} for trigger in triggers]
        return Response({'status': 'success', 'data': trigger_data}, status=status.HTTP_200_OK)

class ScenarioManagerNews(APIView):
    def get(self, request, scenario_manager_id, *args, **kwargs):
        scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
        news = scenario_manager.news.all()
        news_data = [{'id': news_item.id, 'title': news_item.title} for news_item in news]
        return Response({'status': 'success', 'data': news_data}, status=status.HTTP_200_OK)

class ChangeScenarioManagerState(APIView):
    def post(self, request, scenario_manager_id, *args, **kwargs):
        scenario_manager = get_object_or_404(ScenarioManager, id=scenario_manager_id)
        current_state = scenario_manager.state
        new_state = request.data.get('new_state')

        # Define valid transitions, including the rule that allows going back to ONGOING from STOPPED
        valid_transitions = {
            ScenarioManager.ScenarioState.INITIALIZED: [ScenarioManager.ScenarioState.CREATED],
            ScenarioManager.ScenarioState.CREATED: [ScenarioManager.ScenarioState.PUBLISHED],
            ScenarioManager.ScenarioState.PUBLISHED: [ScenarioManager.ScenarioState.ONGOING],
            ScenarioManager.ScenarioState.ONGOING: [ScenarioManager.ScenarioState.STOPPED],
            ScenarioManager.ScenarioState.STOPPED: [ScenarioManager.ScenarioState.FINISHED,
                                                    ScenarioManager.ScenarioState.ONGOING]
            # Allow transition back to ONGOING
        }

        if new_state not in valid_transitions.get(current_state, []):
            return Response(
                {'status': 'error', 'message': f'Invalid state transition from {current_state} to {new_state}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        scenario_manager.state = new_state
        scenario_manager.save()

        return Response(
            {
                'status': 'success',
                'message': f'ScenarioManager state changed successfully to {new_state}',
                'data': self.serialize_scenario_manager(scenario_manager)
            },
            status=status.HTTP_200_OK
        )

    def serialize_scenario_manager(self, scenario_manager):
        return {
            'id': scenario_manager.id,
            'scenario': scenario_manager.scenario.name,
            'state': scenario_manager.state,
            'stocks': [stock.ticker for stock in scenario_manager.stocks.all()],
            'teams': [team.name for team in scenario_manager.teams.all()],
            'events': [event.name for event in scenario_manager.events.all()],
            'triggers': [trigger.name for trigger in scenario_manager.triggers.all()],
            'news': [news_item.title for news_item in scenario_manager.news.all()],
            'simulation_settings': SimulationSettingsSerializer(scenario_manager.simulation_settings).data if scenario_manager.simulation_settings else None,
            'timestamp': scenario_manager.timestamp,
            'published_date': scenario_manager.published_date
        }