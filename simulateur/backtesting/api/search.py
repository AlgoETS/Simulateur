from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backtesting.models import Chart
from backtesting.serializers import ChartSerializer
class SearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            charts = Chart.objects.filter(backtest__strategy__name__icontains=query)
        else:
            charts = Chart.objects.none()

        serializer = ChartSerializer(charts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
