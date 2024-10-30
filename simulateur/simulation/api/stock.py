from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from simulation.models import Stock, StockPriceHistory, Company, Simulation


class StockManagement(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data

        # Extract stock data
        company_id = data.get('company')
        ticker = data.get('ticker')
        volatility = data.get('volatility', 0.0)
        liquidity = data.get('liquidity', 0.0)

        if not company_id or not ticker:
            return Response(
                {'status': 'error', 'message': 'Company ID and ticker are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        company = get_object_or_404(Company, id=company_id)

        # Create the Stock
        stock = Stock.objects.create(
            company=company,
            ticker=ticker,
            volatility=volatility,
            liquidity=liquidity
        )

        return Response(
            {
                'status': 'success',
                'message': 'Stock created successfully',
                'data': {
                    'id': stock.id,
                    'company': stock.company.name,
                    'ticker': stock.ticker,
                    'volatility': stock.volatility,
                    'liquidity': stock.liquidity,
                    'timestamp': stock.timestamp
                }
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request, stock_id, *args, **kwargs):
        stock = get_object_or_404(Stock, id=stock_id)
        data = request.data

        # Update stock data
        stock.ticker = data.get('ticker', stock.ticker)
        stock.volatility = data.get('volatility', stock.volatility)
        stock.liquidity = data.get('liquidity', stock.liquidity)

        stock.save()

        return Response(
            {
                'status': 'success',
                'message': 'Stock updated successfully',
                'data': {
                    'id': stock.id,
                    'company': stock.company.name,
                    'ticker': stock.ticker,
                    'volatility': stock.volatility,
                    'liquidity': stock.liquidity,
                    'timestamp': stock.timestamp
                }
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, stock_id, *args, **kwargs):
        stock = get_object_or_404(Stock, id=stock_id)
        stock.delete()
        return Response(
            {'status': 'success', 'message': 'Stock deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, stock_id=None, *args, **kwargs):
        if stock_id:
            stock = get_object_or_404(Stock, id=stock_id)
            stock_data = {
                'id': stock.id,
                'company': stock.company.name,
                'ticker': stock.ticker,
                'volatility': stock.volatility,
                'liquidity': stock.liquidity,
                'timestamp': stock.timestamp
            }
            return Response({'status': 'success', 'data': stock_data}, status=status.HTTP_200_OK)

        stocks = Stock.objects.all()
        stock_data = [{
            'id': stock.id,
            'company': stock.company.name,
            'ticker': stock.ticker,
            'volatility': stock.volatility,
            'liquidity': stock.liquidity,
            'timestamp': stock.timestamp
        } for stock in stocks]

        return Response({'status': 'success', 'data': stock_data}, status=status.HTTP_200_OK)


class StockPriceHistoryView(APIView):
    def get(self, request, stock_id, *args, **kwargs):
        simulation_manager_id = request.query_params.get('simulation_manager_id')
        if not simulation_manager_id:
            return Response({'status': 'error', 'message': 'Simulation manager ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        simulation_manager = get_object_or_404(Simulation, id=simulation_manager_id)
        stock = get_object_or_404(Stock, id=stock_id, company__simulation_manager=simulation_manager)

        price_histories = StockPriceHistory.objects.filter(stock=stock).order_by('timestamp')
        price_history_data = [{
            'timestamp': price_history.timestamp,
            'open_price': price_history.open_price,
            'high_price': price_history.high_price,
            'low_price': price_history.low_price,
            'close_price': price_history.close_price
        } for price_history in price_histories]

        return Response({'status': 'success', 'data': price_history_data}, status=status.HTTP_200_OK)