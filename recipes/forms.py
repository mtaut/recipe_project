from django import forms
from .models import Recipe

# form for ingredient search and chart generation
class RecipeSearchForm(forms.Form):
    ingredient = forms.CharField(max_length=120)    
    chart_type = forms.ChoiceField(
        choices=[('', 'Select chart type'), ('#1', 'Bar chart'), ('#2', 'Pie chart'), ('#3', 'Line chart')],
        required=False,        
    )

# form for user to create recipe
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'description', 'pic']