# simulation/api/data_modification.py
from rest_framework import viewsets
from simulation.models import SimulationData
from simulation.serializers import  SimulationDataSerializer

class SimulationDataViewSet(viewsets.ModelViewSet):
    queryset = SimulationData.objects.all()
    serializer_class = SimulationDataSerializer
