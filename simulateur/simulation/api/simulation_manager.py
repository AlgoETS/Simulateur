from datetime import timezone

from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from simulation.models import SimulationManager, Scenario, Stock, Team, Event, Trigger, News, SimulationSettings
from simulation.serializers import SimulationSettingsSerializer


class SimulationManagerManagement(APIView):

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

        simulation_manager = SimulationManager.objects.create(
            scenario=scenario,
            simulation_settings=simulation_settings,
            state=data.get('state', SimulationManager.ScenarioState.INITIALIZED)
        )

        simulation_manager.stocks.set(stocks)
        simulation_manager.teams.set(teams)
        simulation_manager.events.set(events)
        simulation_manager.triggers.set(triggers)
        simulation_manager.news.set(news)

        return Response(
            {
                'status': 'success',
                'message': 'SimulationManager created successfully',
                'data': self.serialize_simulation_manager(simulation_manager)
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request, simulation_manager_id=None, *args, **kwargs):
        if simulation_manager_id:
            simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
            return Response(
                {'status': 'success', 'data': self.serialize_simulation_manager(simulation_manager)},
                status=status.HTTP_200_OK
            )
        else:
            simulation_managers = SimulationManager.objects.all()
            data = [self.serialize_simulation_manager(sm) for sm in simulation_managers]
            return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)

    def put(self, request, simulation_manager_id, *args, **kwargs):
        simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
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
        simulation_manager.stocks.set(stocks)

        # Link teams
        teams = Team.objects.filter(id__in=team_ids)
        simulation_manager.teams.set(teams)

        # Link events
        events = Event.objects.filter(id__in=event_ids)
        simulation_manager.events.set(events)

        # Link triggers
        triggers = Trigger.objects.filter(id__in=trigger_ids)
        simulation_manager.triggers.set(triggers)

        # Link news
        news = News.objects.filter(id__in=news_ids)
        simulation_manager.news.set(news)

        # Update SimulationSettings if provided
        if simulation_settings_data and simulation_manager.simulation_settings:
            for key, value in simulation_settings_data.items():
                setattr(simulation_manager.simulation_settings, key, value)
            simulation_manager.simulation_settings.save()

        # Update state
        simulation_manager.state = data.get('state', simulation_manager.state)
        simulation_manager.save()

        return Response(
            {
                'status': 'success',
                'message': 'SimulationManager updated successfully',
                'data': self.serialize_simulation_manager(simulation_manager)
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, simulation_manager_id, *args, **kwargs):
        simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
        simulation_manager.delete()
        return Response(
            {'status': 'success', 'message': 'SimulationManager deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def serialize_simulation_manager(self, simulation_manager):
        return {
            'id': simulation_manager.id,
            'scenario': simulation_manager.scenario.name,
            'state': simulation_manager.state,
            'stocks': [stock.ticker for stock in simulation_manager.stocks.all()],
            'teams': [team.name for team in simulation_manager.teams.all()],
            'events': [event.name for event in simulation_manager.events.all()],
            'triggers': [trigger.name for trigger in simulation_manager.triggers.all()],
            'news': [news_item.title for news_item in simulation_manager.news.all()],
            'simulation_settings': SimulationSettingsSerializer(simulation_manager.simulation_settings).data if simulation_manager.simulation_settings else None,
            'timestamp': simulation_manager.timestamp,
            'published_date': simulation_manager.published_date
        }

class SimulationManagerStocks(APIView):
    def get(self, request, simulation_manager_id, *args, **kwargs):
        simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
        stocks = simulation_manager.stocks.all()
        stock_data = [{'id': stock.id, 'ticker': stock.ticker} for stock in stocks]
        return Response({'status': 'success', 'data': stock_data}, status=status.HTTP_200_OK)

class SimulationManagerTeams(APIView):
    def get(self, request, simulation_manager_id, *args, **kwargs):
        simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
        teams = simulation_manager.teams.all()
        team_data = [{'id': team.id, 'name': team.name} for team in teams]
        return Response({'status': 'success', 'data': team_data}, status=status.HTTP_200_OK)

class SimulationManagerEvents(APIView):
    def get(self, request, simulation_manager_id, *args, **kwargs):
        simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
        events = simulation_manager.events.all()
        event_data = [{'id': event.id, 'name': event.name} for event in events]
        return Response({'status': 'success', 'data': event_data}, status=status.HTTP_200_OK)

class SimulationManagerTriggers(APIView):
    def get(self, request, simulation_manager_id, *args, **kwargs):
        simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
        triggers = simulation_manager.triggers.all()
        trigger_data = [{'id': trigger.id, 'name': trigger.name} for trigger in triggers]
        return Response({'status': 'success', 'data': trigger_data}, status=status.HTTP_200_OK)

class SimulationManagerNews(APIView):
    def get(self, request, simulation_manager_id, *args, **kwargs):
        simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
        news = simulation_manager.news.all()
        news_data = [{'id': news_item.id, 'title': news_item.title} for news_item in news]
        return Response({'status': 'success', 'data': news_data}, status=status.HTTP_200_OK)

class ChangeSimulationManagerState(APIView):
    def post(self, request, simulation_manager_id, *args, **kwargs):
        simulation_manager = get_object_or_404(SimulationManager, id=simulation_manager_id)
        current_state = simulation_manager.state
        new_state = request.data.get('new_state')

        # Define valid transitions, including the rule that allows going back to ONGOING from STOPPED
        valid_transitions = {
            SimulationManager.ScenarioState.INITIALIZED: [SimulationManager.ScenarioState.CREATED],
            SimulationManager.ScenarioState.CREATED: [SimulationManager.ScenarioState.PUBLISHED],
            SimulationManager.ScenarioState.PUBLISHED: [SimulationManager.ScenarioState.ONGOING],
            SimulationManager.ScenarioState.ONGOING: [SimulationManager.ScenarioState.STOPPED],
            SimulationManager.ScenarioState.STOPPED: [SimulationManager.ScenarioState.FINISHED,
                                                    SimulationManager.ScenarioState.ONGOING]
            # Allow transition back to ONGOING
        }

        if new_state not in valid_transitions.get(current_state, []):
            return Response(
                {'status': 'error', 'message': f'Invalid state transition from {current_state} to {new_state}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        simulation_manager.state = new_state
        simulation_manager.save()

        return Response(
            {
                'status': 'success',
                'message': f'SimulationManager state changed successfully to {new_state}',
                'data': self.serialize_simulation_manager(simulation_manager)
            },
            status=status.HTTP_200_OK
        )

    def serialize_simulation_manager(self, simulation_manager):
        return {
            'id': simulation_manager.id,
            'scenario': simulation_manager.scenario.name,
            'state': simulation_manager.state,
            'stocks': [stock.ticker for stock in simulation_manager.stocks.all()],
            'teams': [team.name for team in simulation_manager.teams.all()],
            'events': [event.name for event in simulation_manager.events.all()],
            'triggers': [trigger.name for trigger in simulation_manager.triggers.all()],
            'news': [news_item.title for news_item in simulation_manager.news.all()],
            'simulation_settings': SimulationSettingsSerializer(simulation_manager.simulation_settings).data if simulation_manager.simulation_settings else None,
            'timestamp': simulation_manager.timestamp,
            'published_date': simulation_manager.published_date
        }