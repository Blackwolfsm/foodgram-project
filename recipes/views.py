from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .models import Recipe, Ingredient, User, RecipeIngredient, Follow, RecipeFavorites, ShoppingList
from .forms import RecipeForm
from .utils import parse_name_amount_ingredients


def index(request):
    recipes_list = Recipe.objects.all()
    return render(request, 'index.html', 
                  {'recipes_list': recipes_list})


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        list_inrgidients = parse_name_amount_ingredients(request.POST)
        print(request.POST)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            for ingr_amount in list_inrgidients:
                new_recipe.ingredients.add(
                    Ingredient.objects.get(name=ingr_amount[0]),    
                    through_defaults={'amount': ingr_amount[1]}
                )
            return render(request, 'customPage.html', {'text': 'Ваш рецепт создан'})
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


def recipe_view(request, username, recipe_id):
    author_recipe = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    return render(request, 'viewRecipe.html',
                  {'author': author_recipe,
                  'recipe': recipe,
                  'ingredients': ingredients})


def shoplist_view(request):
    recipe_in_basket = []
    shoplist = request.user.shop_list.all()
    if shoplist:
        recipe_in_basket = Recipe.objects.filter(
            id__in=shoplist.values('recipe_id'))

    return render(request, 'shopList.html', {'recipes': recipe_in_basket})


def page_not_found(request, exception):
    return render(request, 'customPage.html',
                  {'text': 'Страница не найдена'}, status=404)


def server_error(request):
    return render(
        request, 'customPage.html',
        {'text': 'Ошибка на сервере, попробуйте обновить страницу'},
        status=500)