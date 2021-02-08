from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Ingredient, Recipe, RecipeIngredient, User
from .utils import (filtering_by_tags, generate_content_shoplist, get_tags,
                    parse_name_amount_ingredients)


def index(request):
    recipes_list = Recipe.objects.all()
    tags = get_tags(request)
    if tags:
        recipes_list = filtering_by_tags(recipes_list, tags)
    paginator = Paginator(recipes_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/index.html',
                  {'page': page, 'paginator': paginator, 'tags': tags,
                   'index': True})


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, request.FILES or None)
    list_inrgidients = parse_name_amount_ingredients(request.POST)
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.save()
        for ingr_amount in list_inrgidients:
            new_recipe.ingredients.add(
                Ingredient.objects.get(name=ingr_amount[0]),
                through_defaults={'amount': ingr_amount[1]}
            )
        return render(request, 'tool/customPage.html',
                      {'text': 'Ваш рецепт создан'})
    return render(request, 'recipes/formRecipe.html',
                  {'form': form, 'new_recipe': True})


@login_required
def edit_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', recipe.author.username, recipe.id)
    form = RecipeForm(request.POST or None,
                      request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        form.save()
        recipe.recipeingredient_set.all().delete()
        list_inrgidients = parse_name_amount_ingredients(request.POST)
        for ingr_amount in list_inrgidients:
            recipe.ingredients.add(
                Ingredient.objects.get(name=ingr_amount[0]),
                through_defaults={'amount': ingr_amount[1]}
            )
        return render(request, 'tool/customPage.html',
                      {'text': 'Ваш рецепт отредактирован'})
    return render(request, 'recipes/formRecipe.html',
                  {'form': form, 'recipe': recipe, 'new_recipe': True})


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    ingredients = recipe.recipeingredient_set.all()
    return render(request, 'recipes/viewRecipe.html',
                  {'recipe': recipe,
                   'ingredients': ingredients})


@login_required
def shoplist_view(request):
    shoplist = request.user.shop_list.all()

    return render(request, 'recipes/shopList.html',
                  {'shopinglist': shoplist, 'shoplist': True})


@login_required
def get_shoplist(request):
    user = request.user
    check_shoplist = user.shop_list.all().exists()
    ingredients_in_basket = []
    if check_shoplist:
        shoplist = user.shop_list.all()
        ingredients_in_basket = RecipeIngredient.objects.filter(
            recipe_id__in=shoplist.values('recipe_id'))
    else:
        return render(
            request, 'tool/customPage.html',
            {'text': 'Ваш список покупок пуст'})
    content = generate_content_shoplist(ingredients_in_basket)
    response = HttpResponse(content, content_type='application/txt')
    response['Content-Disposition'] = 'attachment; filename=shoplist.txt'
    return response


@login_required
def favorites_view(request):
    favorites_recipe = Recipe.objects.filter(
        id__in=request.user.recipes_favorites.values(
            'recipe_id')
    )
    tags = get_tags(request)
    if tags:
        favorites_recipe = filtering_by_tags(favorites_recipe, tags)
    paginator = Paginator(favorites_recipe, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/favorites.html',
                  {'page': page, 'paginator': paginator, 'tags': tags,
                   'favorites': True})


@login_required
def follow_view(request):
    authors = User.objects.filter(
        id__in=request.user.follower.values('author_id')
    )
    paginator = Paginator(authors, settings.AUTHORS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/myFollow.html',
                  {'page': page, 'paginator': paginator, 'follow': True})


def profile_view(request, username):
    author = get_object_or_404(User, username=username)
    recipes_list = author.author_recipes.all()
    tags = get_tags(request)
    if tags:
        recipes_list = filtering_by_tags(recipes_list, tags)
    paginator = Paginator(recipes_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/authorRecipe.html',
                  {'page': page, 'paginator': paginator,
                   'tags': tags, 'author': author,
                   'index': True})
