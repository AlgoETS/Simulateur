import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

FMP_API_KEY = 'your_fmp_api_key_here'  # Add your FMP API key here

class FMPDataAPIView(APIView):
    def get(self, request, ticker):
        try:
            # Fetch the historical data from FMP
            url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FMP_API_KEY}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to fetch data from FMP"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
