from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from simulation.models import Company, Stock

class CompanyManagement(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data

        # Extract company data
        name = data.get('name')
        backstory = data.get('backstory', '')
        sector = data.get('sector', '')
        country = data.get('country', '')
        industry = data.get('industry', '')

        if not name:
            return Response(
                {'status': 'error', 'message': 'Company name is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the Company
        company = Company.objects.create(
            name=name,
            backstory=backstory,
            sector=sector,
            country=country,
            industry=industry
        )

        return Response(
            {
                'status': 'success',
                'message': 'Company created successfully',
                'data': {
                    'id': company.id,
                    'name': company.name,
                    'backstory': company.backstory,
                    'sector': company.sector,
                    'country': company.country,
                    'industry': company.industry,
                    'timestamp': company.timestamp
                }
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request, company_id, *args, **kwargs):
        company = get_object_or_404(Company, id=company_id)
        data = request.data

        # Update company data
        company.name = data.get('name', company.name)
        company.backstory = data.get('backstory', company.backstory)
        company.sector = data.get('sector', company.sector)
        company.country = data.get('country', company.country)
        company.industry = data.get('industry', company.industry)

        company.save()

        return Response(
            {
                'status': 'success',
                'message': 'Company updated successfully',
                'data': {
                    'id': company.id,
                    'name': company.name,
                    'backstory': company.backstory,
                    'sector': company.sector,
                    'country': company.country,
                    'industry': company.industry,
                    'timestamp': company.timestamp
                }
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, company_id, *args, **kwargs):
        company = get_object_or_404(Company, id=company_id)
        company.delete()
        return Response(
            {'status': 'success', 'message': 'Company deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, company_id=None, *args, **kwargs):
        if company_id:
            company = get_object_or_404(Company, id=company_id)
            company_data = {
                'id': company.id,
                'name': company.name,
                'backstory': company.backstory,
                'sector': company.sector,
                'country': company.country,
                'industry': company.industry,
                'timestamp': company.timestamp
            }
            return Response({'status': 'success', 'data': company_data}, status=status.HTTP_200_OK)

        companies = Company.objects.all()
        company_data = [{
            'id': company.id,
            'name': company.name,
            'backstory': company.backstory,
            'sector': company.sector,
            'country': company.country,
            'industry': company.industry,
            'timestamp': company.timestamp
        } for company in companies]

        return Response({'status': 'success', 'data': company_data}, status=status.HTTP_200_OK)