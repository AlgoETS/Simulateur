# simulation/api/simulation.py
import json
import logging
from rest_framework import generics, views
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from simulation.models import Scenario, SimulationSettings
from simulation.logic.simulation_manager import SimulationManagerSingleton
from simulation.serializers import SimulationSettingsSerializer

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class SimulationSettingsView(generics.RetrieveUpdateAPIView):
    queryset = SimulationSettings.objects.all()
    serializer_class = SimulationSettingsSerializer

@method_decorator(csrf_exempt, name='dispatch')
class StartSimulation(views.APIView):
    def post(self, request):
        data = request.data
        scenario_id = data.get('scenario_id')
        time_unit = data.get('time_unit', 'second')

        simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
        simulation_manager.start_simulation(time_unit)

        return Response({'status': 'success'})

@method_decorator(csrf_exempt, name='dispatch')
class PauseSimulation(views.APIView):
    def post(self, request):
        data = request.data
        scenario_id = data.get('scenario_id')

        simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
        simulation_manager.pause_simulation()

        return Response({'status': 'paused'})

@method_decorator(csrf_exempt, name='dispatch')
class StopSimulation(views.APIView):
    def post(self, request):
        data = request.data
        scenario_id = data.get('scenario_id')

        simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
        simulation_manager.stop_simulation()

        SimulationManagerSingleton.remove_instance(scenario_id)
        return Response({'status': 'stopped'})

@method_decorator(csrf_exempt, name='dispatch')
class FastForwardSimulation(views.APIView):
    def post(self, request):
        data = request.data
        scenario_id = data.get('scenario_id')

        simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
        simulation_manager.fast_forward_simulation()

        return Response({'status': 'fast-forwarded'})

@method_decorator(csrf_exempt, name='dispatch')
class RewindSimulation(views.APIView):
    def post(self, request):
        data = request.data
        scenario_id = data.get('scenario_id')

        simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
        simulation_manager.rewind_simulation()

        return Response({'status': 'rewinded'})
