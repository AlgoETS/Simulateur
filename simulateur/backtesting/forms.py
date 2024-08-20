from django import forms
from .models import Strategy

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'description', 'parameters']  # Adjust based on your Strategy model
        widgets = {
            'parameters': forms.Textarea(attrs={'rows': 3}),
        }
