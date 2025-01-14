import json
import logging
import os

import ollama
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from simulation.models import Company, Stock, News, Scenario

logger = logging.getLogger(__name__)


def check_ollama_service():
    model_name = os.environ.get('OLLAMA_MODEL', 'llama3')
    try:
        response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': 'Test message'}])
        return True
    except ollama.ResponseError as e:
        if e.status_code == 404 and f'model {model_name} not found' in e.error:
            return True
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": "Ollama service is unavailable or another error occurred: " + str(e)}


class InteractWithOllama(APIView):
    def post(self, request):
        service_check = check_ollama_service()
        if service_check is not True:
            return Response(service_check, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        data = request.data.get('data', '')
        model_name = os.environ.get('OLLAMA_MODEL', 'llama3')

        try:
            response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': data}])
            return Response({'status': 'success', 'data': response['message']['content']})
        except ollama.ResponseError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateNewsAI(APIView):
    def post(self, request):
        service_check = check_ollama_service()
        if service_check is not True:
            return Response(service_check, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        company_id = request.data.get('company_id')
        stock_id = request.data.get('stock_id')

        company = get_object_or_404(Company, id=company_id)
        stock = get_object_or_404(Stock, id=stock_id)

        prompt = (
            f"Generate a fake tweet about {company.name}, a company in the {company.sector} sector based in {company.country}. "
            f"Mention their stock ticker {stock.ticker}. Make it engaging and suitable for social media."
        )

        model_name = os.environ.get('OLLAMA_MODEL', 'llama3')

        try:
            response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
            tweet_content = response['message']['content']

            news_data = {
                'title': f"News about {company.name} ({stock.ticker})",
                'content': tweet_content,
                'company': company,
                'published_date': timezone.now()
            }
            News.objects.create(**news_data)
            return Response({'status': 'success', 'data': news_data})
        except ollama.ResponseError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateEventAI(APIView):
    def post(self, request):
        service_check = check_ollama_service()
        if service_check is not True:
            return Response(service_check, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        company_id = request.data.get('company_id')
        stock_id = request.data.get('stock_id')

        company = get_object_or_404(Company, id=company_id)
        stock = get_object_or_404(Stock, id=stock_id)

        prompt = (
            f"Generate a news headline about {company.name}, a company in the {company.sector} sector based in {company.country}. "
            f"Mention their stock ticker {stock.ticker}. Make it engaging and suitable for a news article."
        )

        model_name = os.environ.get('OLLAMA_MODEL', 'llama3')

        try:
            response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
            event_data = {
                'title': f"Event about {company.name} ({stock.ticker})",
                'description': response['message']['content'],
                'company': company,
                'published_date': timezone.now()
            }
            return Response({'status': 'success', 'data': event_data})
        except ollama.ResponseError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateTriggerAI(APIView):
    def post(self, request):
        service_check = check_ollama_service()
        if service_check is not True:
            return Response(service_check, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        company_id = request.data.get('company_id')
        stock_id = request.data.get('stock_id')

        company = get_object_or_404(Company, id=company_id)
        stock = get_object_or_404(Stock, id=stock_id)

        prompt = (
            f"Generate a trigger event for {company.name}, a company in the {company.sector} sector based in {company.country}. "
            f"Mention their stock ticker {stock.ticker}. Make it engaging and suitable for a trigger event."
        )

        model_name = os.environ.get('OLLAMA_MODEL', 'llama3')

        try:
            response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
            trigger_data = {
                'title': f"Trigger event for {company.name} ({stock.ticker})",
                'description': response['message']['content'],
                'company': company,
                'published_date': timezone.now()
            }
            return Response({'status': 'success', 'data': trigger_data})
        except ollama.ResponseError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateCompanyAndStockAI(APIView):
    def post(self, request):
        service_check = check_ollama_service()
        if service_check is not True:
            return Response(service_check, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        prompt = (
            "Generate a new company and stock with the following details:\n"
            "1. Company name, backstory, sector, country, and industry.\n"
            "2. Stock details including ticker\n\n"
            "@startuml\n"
            "class Company {\n"
            "  + CharField name(max_length=100, default='')\n"
            "  + TextField backstory(default='')\n"
            "  + CharField sector(max_length=100, default='')\n"
            "  + CharField country(max_length=100, default='')\n"
            "  + CharField industry(max_length=100, default='')\n"
            "  + DateTimeField timestamp(auto_now_add=True)\n"
            "}\n"
            "class Stock {\n"
            "  + ForeignKey company('Company', on_delete=models.CASCADE, related_name='stocks')\n"
            "  + CharField ticker(max_length=10, default='')\n"
            "  + FloatField price(default=0.0)\n"
            "  + FloatField open_price(default=0.0)\n"
            "  + FloatField high_price(default=0.0)\n"
            "  + FloatField low_price(default=0.0)\n"
            "  + FloatField close_price(default=0.0)\n"
            "  + FloatField partial_share(default=0.0)\n"
            "  + IntegerField complete_share(default=0)\n"
            "  + DateTimeField timestamp(auto_now_add=True)\n"
            "}\n"
            "Company --> Stock\n"
            "@enduml"
        )

        model_name = os.environ.get('OLLAMA_MODEL', 'llama3')

        try:
            response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
            ai_response = response['message']['content']

            logger.info(f"AI Response: {ai_response}")

            company_data, stock_data = self.parse_company_stock_data(ai_response)
            company = Company.objects.create(**company_data)
            stock_data['company'] = company
            Stock.objects.create(**stock_data)
            return Response({'status': 'success', 'company': company_data, 'stock': stock_data},
                            status=status.HTTP_201_CREATED)
        except ollama.ResponseError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return Response({'status': 'error', 'message': 'Invalid JSON response from AI model'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'status': 'error', 'message': 'An unexpected error occurred'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse_company_stock_data(self, ai_response):
        logger.debug(f"Raw AI Response: {ai_response}")
        data = json.loads(ai_response)
        company_data = {
            'name': data['company_name'],
            'backstory': data['company_backstory'],
            'sector': data['company_sector'],
            'country': data['company_country'],
            'industry': data['company_industry'],
        }
        stock_data = {
            'ticker': data['stock_ticker'],
            'price': data['stock_price'],
            'open_price': data['stock_open_price'],
            'high_price': data['stock_high_price'],
            'low_price': data['stock_low_price'],
            'close_price': data['stock_close_price'],
            'partial_share': data['stock_partial_share'],
            'complete_share': data['stock_complete_share']
        }
        return company_data, stock_data


class CreateScenarioAI(APIView):
    def post(self, request, *args, **kwargs):
        service_check = check_ollama_service()
        if service_check is not True:
            return Response(service_check, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        model_name = os.environ.get('OLLAMA_MODEL', 'llama3')
        prompt = (
            "Generate a new simulation scenario with the following details in JSON format:\n"
            "{\n"
            "  \"scenario_name\": \"<Scenario Name>\",\n"
            "  \"description\": \"<Description>\",\n"
            "  \"timer_step\": \"<Timer Step>\",\n"
            "  \"timer_step_unit\": \"<Timer Step Unit>\",\n"
            "  \"companies\": [\n"
            "    {\n"
            "      \"name\": \"<Company Name>\",\n"
            "      \"backstory\": \"<Backstory>\",\n"
            "      \"sector\": \"<Sector>\",\n"
            "      \"country\": \"<Country>\",\n"
            "      \"industry\": \"<Industry>\",\n"
            "      \"stock\": {\n"
            "        \"ticker\": \"<Ticker>\",\n"
            "        \"price\": <Price>,\n"
            "        \"open_price\": <Open Price>,\n"
            "        \"high_price\": <High Price>,\n"
            "        \"low_price\": <Low Price>,\n"
            "        \"close_price\": <Close Price>,\n"
            "        \"partial_share\": <Partial Share>,\n"
            "        \"complete_share\": <Complete Share>\n"
            "      }\n"
            "    },\n"
            "    // Repeat for 2 more companies\n"
            "  ]\n"
            "}\n"
        )

        try:
            response = ollama.chat(
                model=model_name,
                messages=[{'role': 'user', 'content': prompt}],
                stream=False,
            )
            ai_response = response['message']['content']

            logger.info(f"AI Response: {ai_response}")

            scenario_details = self.extract_json_from_response(ai_response)
            scenario = Scenario.objects.create(
                scenario_name=scenario_details['scenario_name'],
                description=scenario_details['description'],
                timer_step=scenario_details['timer_step'],
                timer_step_unit=scenario_details['timer_step_unit']
            )

            for company_data in scenario_details['companies']:
                company = Company.objects.create(
                    name=company_data['name'],
                    backstory=company_data['backstory'],
                    sector=company_data['sector'],
                    country=company_data['country'],
                    industry=company_data['industry'],
                )
                stock_data = company_data['stock']
                Stock.objects.create(
                    company=company,
                    ticker=stock_data['ticker'],
                    price=stock_data['price'],
                    open_price=stock_data['open_price'],
                    high_price=stock_data['high_price'],
                    low_price=stock_data['low_price'],
                    close_price=stock_data['close_price'],
                    partial_share=stock_data['partial_share'],
                    complete_share=stock_data['complete_share']
                )
                scenario.companies.add(company)

            return Response({'status': 'success', 'data': scenario_details}, status=status.HTTP_201_CREATED)
        except ollama.ResponseError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'status': 'error', 'message': 'An unexpected error occurred'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_json_from_response(self, ai_response):
        try:
            start_index = ai_response.find('{')
            end_index = ai_response.rfind('}') + 1
            if start_index != -1 and end_index != -1:
                json_data = ai_response[start_index:end_index]
                return json.loads(json_data)
            else:
                raise ValueError("JSON object not found in response")
        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"JSON decode error: {str(e)}")
            return {}

    def extract_value(self, line, key):
        try:
            return line.split(f"**{key}:**")[1].strip()
        except IndexError:
            return ''

    def parse_price(self, price_str):
        price_str = \
        price_str.replace('$', '').replace('€', '').replace('£', '').replace(',', '').replace('USD', '').replace('CAD',
                                                                                                                 '').split(
            ' ')[0]
        return float(price_str)
