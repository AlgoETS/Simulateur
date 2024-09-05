import httpx
from httpx import HTTPStatusError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from yahoofinancials import YahooFinancials
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ExternalAPIBaseView(APIView):
    """
    Base view to handle common logic for external API requests using httpx asynchronously.
    """

    async def handle_request(self, url):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()  # Raises an HTTPStatusError for bad responses
                return response.json()
        except HTTPStatusError as e:
            raise Exception(f"HTTP error occurred: {str(e)}")
        except httpx.RequestError as e:
            raise Exception(f"Error occurred while making the request: {str(e)}")


class FMPDataAPIViewAsync(ExternalAPIBaseView):

    @swagger_auto_schema(
        operation_summary="Get FMP data (async)",
        operation_description="Fetch historical price data from FMP using an asynchronous HTTP request.",
        responses={200: openapi.Response(description="Successful Response")}
    )
    async def get(self, request, ticker):
        try:
            FMP_API_KEY = config('FMP_API_KEY')
            url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FMP_API_KEY}'
            data = await self.handle_request(url)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FMPDataAPIVIewSync(APIView):

    @swagger_auto_schema(
        operation_summary="Get FMP data (sync)",
        operation_description="Fetch historical price data from FMP using a synchronous HTTP request.",
        responses={200: openapi.Response(description="Successful Response")}
    )
    def get(self, request, ticker):
        try:
            FMP_API_KEY = config('FMP_API_KEY')
            url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FMP_API_KEY}'
            response = httpx.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except HTTPStatusError as e:
            return Response({"error": f"HTTP error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except httpx.RequestError as e:
            return Response({"error": f"Error occurred while making the request: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CoinGeckoDataAPIViewAsync(ExternalAPIBaseView):

    @swagger_auto_schema(
        operation_summary="Get CoinGecko data (async)",
        operation_description="Fetch cryptocurrency data from CoinGecko using an asynchronous HTTP request.",
        responses={200: openapi.Response(description="Successful Response")}
    )
    async def get(self, request, crypto_id):
        try:
            COINGECKO_BASE_URL = 'https://api.coingecko.com/api/v3'
            url = f'{COINGECKO_BASE_URL}/coins/{crypto_id}/market_chart?vs_currency=usd&days=30'
            data = await self.handle_request(url)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CoinGeckoDataAPIViewSync(APIView):

    @swagger_auto_schema(
        operation_summary="Get CoinGecko data (sync)",
        operation_description="Fetch cryptocurrency data from CoinGecko using a synchronous HTTP request.",
        responses={200: openapi.Response(description="Successful Response")}
    )
    def get(self, request, crypto_id):
        try:
            COINGECKO_BASE_URL = 'https://api.coingecko.com/api/v3'
            url = f'{COINGECKO_BASE_URL}/coins/{crypto_id}/market_chart?vs_currency=usd&days=30'
            response = httpx.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except HTTPStatusError as e:
            return Response({"error": f"HTTP error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except httpx.RequestError as e:
            return Response({"error": f"Error occurred while making the request: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class YFinanceDataAPIViewAsync(APIView):

    @swagger_auto_schema(
        operation_summary="Get YFinance data (async)",
        operation_description="Fetch stock data from Yahoo Finance using an asynchronous HTTP request.",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date in YYYY-MM-DD format", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date in YYYY-MM-DD format", type=openapi.TYPE_STRING),
            openapi.Parameter('interval', openapi.IN_QUERY, description="Time interval (e.g., daily, weekly, monthly)", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response(description="Successful Response")}
    )
    async def get(self, request, ticker):
        start_date = request.GET.get('start_date', '2018-08-01')  # Default to '2018-08-01' if not provided
        end_date = request.GET.get('end_date', '2018-08-10')  # Default to '2018-08-10' if not provided
        interval = request.GET.get('interval', 'weekly')  # Default to 'weekly' if not provided

        try:
            stock = YahooFinancials(ticker)
            historical_data = stock.get_historical_price_data(start_date, end_date, interval)
            # Check if data is available
            if historical_data and ticker in historical_data and historical_data[ticker]['prices']:
                return Response(historical_data, status=status.HTTP_200_OK)
            else:
                raise Exception("No data found for this ticker")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class YFinanceDataAPIViewSync(APIView):

    @swagger_auto_schema(
        operation_summary="Get YFinance data (sync)",
        operation_description="Fetch stock data from Yahoo Finance using a synchronous HTTP request.",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date in YYYY-MM-DD format", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date in YYYY-MM-DD format", type=openapi.TYPE_STRING),
            openapi.Parameter('interval', openapi.IN_QUERY, description="Time interval (e.g., daily, weekly, monthly)", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response(description="Successful Response")}
    )
    def get(self, request, ticker):
        start_date = request.GET.get('start_date', '2018-08-01')  # Default to '2018-08-01' if not provided
        end_date = request.GET.get('end_date', '2018-08-10')  # Default to '2018-08-10' if not provided
        interval = request.GET.get('interval', 'weekly')  # Default to 'weekly' if not provided

        try:
            stock = YahooFinancials(ticker)
            historical_data = stock.get_historical_price_data(start_date, end_date, interval)
            # Check if data is available
            if historical_data and ticker in historical_data and historical_data[ticker]['prices']:
                return Response(historical_data, status=status.HTTP_200_OK)
            else:
                raise Exception("No data found for this ticker")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)