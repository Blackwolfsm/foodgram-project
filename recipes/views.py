from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Recipe, Ingredient, User, RecipeIngredient, Follow, RecipeFavorites
from .forms import RecipeForm
from .utils import parse_name_amount_ingredients


def index(request):
    recipes_list = Recipe.objects.all()
    recipes_favorites_id = []
    if request.user.is_authenticated:
        list_favorites = request.user.recipes_favorites.all()
        for item in list_favorites.values('recipe_id'):
            recipes_favorites_id.append(item['recipe_id'])
    return render(request, 'index.html', 
                  {'recipes_list': recipes_list,
                   'favorites': recipes_favorites_id})


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
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    check_subscribe = False
    check_favorites = False

    if user.is_authenticated:
        if author_recipe.following.filter(user=user).exists():
            check_subscribe = True
        if user.recipes_favorites.filter(recipe_id=recipe.id).exists():
            check_favorites = True

    return render(request, 'viewRecipe.html',
                  {'author': author_recipe,
                  'recipe': recipe,
                  'ingredients': ingredients,
                  'subscribe': check_subscribe,
                  'favorites': check_favorites})

