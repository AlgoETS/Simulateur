from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Company, Portfolio, Transaction

@login_required
def user_dashboard(request):
    companies = Company.objects.all()
    portfolio = Portfolio.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    context = {
        'companies': companies,
        'portfolio': portfolio,
        'transactions': transactions,
    }
    return render(request, 'simulation/user_dashboard.html', context)
