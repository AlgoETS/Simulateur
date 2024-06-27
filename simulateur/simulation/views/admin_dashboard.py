from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Scenario, Game

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    scenarios = Scenario.objects.all()
    games = Game.objects.all()
    context = {
        'scenarios': scenarios,
        'games': games,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
