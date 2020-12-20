from django.shortcuts import render

from .models import Recipe
from .forms import RecipeForm


def index(request):
    recipes_list = Recipe.objects.all()
    return render(request, 'index.html', 
                  {'recipes_list': recipes_list})


def create_recipe(request):
    """Обрабатывает запрос, если GET, то отдает форму для создания
       рецепта, если POST, то форма проходит валидацию, при успехе 
       сохраняется в базе данных"""
    
    form = RecipeForm()

    return render(request, 'formRecipe.html', {'form': form})
