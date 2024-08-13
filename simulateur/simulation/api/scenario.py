from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from simulation.models import Scenario


class ScenarioManagement(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data

        # Extract scenario data
        name = data.get('name')
        description = data.get('description', '')
        backstory = data.get('backstory', '')
        duration = data.get('duration', 0)

        if not name:
            return Response(
                {'status': 'error', 'message': 'Scenario name is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the Scenario
        scenario = Scenario.objects.create(
            name=name,
            description=description,
            backstory=backstory,
            duration=duration
        )

        return Response(
            {
                'status': 'success',
                'message': 'Scenario created successfully',
                'data': {
                    'id': scenario.id,
                    'name': scenario.name,
                    'description': scenario.description,
                    'backstory': scenario.backstory,
                    'duration': scenario.duration,
                }
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request, scenario_id=None, *args, **kwargs):
        if scenario_id:
            scenario = get_object_or_404(Scenario, id=scenario_id)
            scenario_data = {
                'id': scenario.id,
                'name': scenario.name,
                'description': scenario.description,
                'backstory': scenario.backstory,
                'duration': scenario.duration,
            }
            return Response({'status': 'success', 'data': scenario_data}, status=status.HTTP_200_OK)

        scenarios = Scenario.objects.all()
        scenario_data = [{
            'id': scenario.id,
            'name': scenario.name,
            'description': scenario.description,
            'backstory': scenario.backstory,
            'duration': scenario.duration,
        } for scenario in scenarios]

        return Response({'status': 'success', 'data': scenario_data}, status=status.HTTP_200_OK)

    def put(self, request, scenario_id, *args, **kwargs):
        scenario = get_object_or_404(Scenario, id=scenario_id)
        data = request.data

        # Update scenario data
        scenario.name = data.get('name', scenario.name)
        scenario.description = data.get('description', scenario.description)
        scenario.backstory = data.get('backstory', scenario.backstory)
        scenario.duration = data.get('duration', scenario.duration)

        scenario.save()

        return Response(
            {
                'status': 'success',
                'message': 'Scenario updated successfully',
                'data': {
                    'id': scenario.id,
                    'name': scenario.name,
                    'description': scenario.description,
                    'backstory': scenario.backstory,
                    'duration': scenario.duration,
                }
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, scenario_id, *args, **kwargs):
        scenario = get_object_or_404(Scenario, id=scenario_id)
        scenario.delete()
        return Response(
            {'status': 'success', 'message': 'Scenario deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
