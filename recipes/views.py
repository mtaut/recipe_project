from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView   # to display list and details of recipes
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Recipe                                          # to access Recipe model
from django.contrib.auth.mixins import LoginRequiredMixin           # protecting views (CBV)
from django.contrib.auth.decorators import login_required           # protecting views (FBV)
from .forms import RecipeSearchForm, RecipeForm
from .utils import get_chart
import pandas as pd
from django.db.models import Q

# home page view
def home(request):
    return render(request, 'recipes/recipes_home.html')

# about page view
@login_required
def about_page(request):
    return render(request, 'recipes/about.html')

# recipe list view-displays all recipes, allows for searching, and chart
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'

    # queryset to filter recipes based on search input
    def get_queryset(self):
        queryset = Recipe.objects.all()
        form = RecipeSearchForm(self.request.GET or None)
        
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            if search_query:
                queryset = queryset.filter(ingredients__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RecipeSearchForm(self.request.GET or None)
        context['form'] = form

        search_results = self.get_queryset()
        if search_results.exists():            
            context['search_results'] = search_results

        chart = None
        search_results = None

        # extract all recipes from database
        recipes = Recipe.objects.all()

        if form.is_valid():
            ingredient = form.cleaned_data.get('ingredient')         
            chart_type = form.cleaned_data.get('chart_type')
            
            if ingredient:
                recipes = recipes.filter(Q(ingredients__icontains=ingredient))

            # convert QuerySet to pandas DataFrame
            if recipes.exists() and chart_type:
                df = pd.DataFrame.from_records(
                    recipes.values('ingredients', 'cooking_time')
                )

                # passing data to create the chart
                chart = get_chart(chart_type, df)
            
            search_results = recipes
        
        context['form'] = form
        context['chart'] = chart
        context['search_results'] = search_results
        return context

# displays individual details of recipe
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipes_detail.html'

# allows logged-in users to create a recipe
class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/create_recipe.html'
    success_url = reverse_lazy('recipes:recipes_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Recipe created successfully!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating your recipe. Please check the form.")
        return super().form_valid(form)