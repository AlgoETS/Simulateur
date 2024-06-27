from django.shortcuts import render
from .models import Stock, News

def game_dashboard(request):
    stocks = Stock.objects.all()
    news = News.objects.all()
    context = {
        'stocks': stocks,
        'news': news,
    }
    return render(request, 'simulation/game_dashboard.html', context)
