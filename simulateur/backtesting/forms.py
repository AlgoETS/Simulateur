from django import forms
from .models import Strategy, Backtest, StockBacktest, StrategyOutput, DataSource


class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'description', 'file_name']  # Updated fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'file_name': forms.ClearableFileInput(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
        }


class BacktestForm(forms.ModelForm):
    class Meta:
        model = Backtest
        fields = ['strategy', 'stock', 'start_date', 'end_date', 'status']
        widgets = {
            'strategy': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'stock': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'status': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
        }


class StockBacktestForm(forms.ModelForm):
    class Meta:
        model = StockBacktest
        fields = ['ticker', 'name', 'sector', 'exchange', 'data_source']

    data_source = forms.ModelChoiceField(
        queryset=DataSource.objects.all(),
        empty_label="Select a data source",
        widget=forms.Select(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
    )

class StrategyOutputForm(forms.ModelForm):
    class Meta:
        model = StrategyOutput
        fields = ['strategy', 'ticker', 'output_type', 'file']
        widgets = {
            'strategy': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'ticker': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'output_type': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
            'file': forms.ClearableFileInput(attrs={'class': 'border border-gray-300 rounded-lg w-full p-2'}),
        }
