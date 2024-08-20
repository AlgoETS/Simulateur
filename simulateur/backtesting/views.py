from django.http import HttpResponseRedirect
from .forms import StrategyForm  # Assuming you have a form for creating a strategy

from django.shortcuts import render
from django.views import View
from .models import Strategy, StrategyOutput


class SearchChartView(View):
    template_name = 'search_chart.html'

    def get(self, request):
        strategies = Strategy.objects.all()
        strategy_outputs = StrategyOutput.objects.none()

        selected_strategy_id = request.GET.get('strategy')
        ticker = request.GET.get('ticker')

        if selected_strategy_id and ticker:
            strategy_outputs = StrategyOutput.objects.filter(strategy_id=selected_strategy_id, ticker=ticker)

        context = {
            'strategies': strategies,
            'strategy_outputs': strategy_outputs,
        }
        return render(request, self.template_name, context)


class StrategyManagementView(View):
    def get(self, request):
        form = StrategyForm()
        strategies = Strategy.objects.filter(created_by=request.user)
        context = {
            'form': form,
            'strategies': strategies
        }
        return render(request, 'strategy_management.html', context)

    def post(self, request):
        form = StrategyForm(request.POST)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.created_by = request.user
            strategy.save()
            return HttpResponseRedirect(request.path_info)  # Refresh the page

        # If the form is invalid, re-render the page with existing data and errors
        strategies = Strategy.objects.filter(created_by=request.user)
        context = {
            'form': form,
            'strategies': strategies
        }
        return render(request, 'strategy_management.html', context)
