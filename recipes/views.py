from django.shortcuts import render
from django.http import HttpResponse

from .models import Recipe
from .forms import RecipeForm


def index(request):
    recipes_list = Recipe.objects.all()
    return render(request, 'index.html', 
                  {'recipes_list': recipes_list})


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm()
        return HttpResponse(f'<h1></h1> \n {form}')
    
    return render(request, 'formRecipe.html')


