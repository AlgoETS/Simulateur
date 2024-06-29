from django.shortcuts import render
from django.views import View
from simulation.models import Scenario

class SimulationGraphView(View):
    def get(self, request):
        scenarios = Scenario.objects.all()
        return render(request, 'simulation/graph.html', {'scenarios': scenarios})
