from django.shortcuts import render
from django.http import HttpResponse

from .models import Recipe, Ingredient
from .forms import RecipeForm
from .utils import parse_data_for_recipe


def index(request):
    recipes_list = Recipe.objects.all()
    return render(request, 'index.html', 
                  {'recipes_list': recipes_list})


def create_recipe(request):
    if request.method == 'POST':
        print(request.POST)
        data = parse_data_for_recipe(request.POST)
        Recipe.objects.create(
            author=request.user,
            title=data['title'],
            descriptions=data['descriptions'],
            cooking_time=data['cooking_time'],
            breakfast=data['breakfast'],
            dinner=data['dinner'],
            lunch=data['lunch']
        )
        return HttpResponse('<h1>Рецепт создан</h1>')
    return render(request, 'formRecipe.html')
