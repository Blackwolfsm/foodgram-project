from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Recipe, Ingredient, User, RecipeIngredient, Follow, RecipeFavorites, ShoppingList
from .forms import RecipeForm
from .utils import parse_name_amount_ingredients, generate_content_shoplist, get_tags, filtering_by_tags


def index(request):
    recipes_list = Recipe.objects.all().order_by('-pub_date')
    tags = get_tags(request)
    if tags:
        recipes_list = filtering_by_tags(recipes_list, tags)
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/index.html', 
                  {'page': page, 'paginator': paginator, 'tags': tags})


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
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
            return render(request, 'customPage.html', {'text': 'Ваш рецепт создан'})
    else:
        form = RecipeForm()
    return render(request, 'recipes/formRecipe.html', {'form': form})


@login_required
def edit_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        if request.method == 'POST':
            form = RecipeForm(
                request.POST, files=request.FILES, instance=recipe)
            if form.is_valid:
                form.save()
                return redirect('recipe_view', recipe.author, recipe.id)
        else:
            form = RecipeForm(instance=recipe)
        return render(request, 'recipes/formRecipe.html',
                      {'form': form, 'recipe': recipe})
    return redirect('recipe_view', recipe.author.username, recipe.id)



def recipe_view(request, username, recipe_id):
    author_recipe = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    return render(request, 'recipes/viewRecipe.html',
                  {'author': author_recipe,
                  'recipe': recipe,
                  'ingredients': ingredients})


@login_required
def shoplist_view(request):
    recipe_in_basket = []
    shoplist = request.user.shop_list.all()
    if shoplist:
        recipe_in_basket = Recipe.objects.filter(
            id__in=shoplist.values('recipe_id')).order_by('-pub_date')

    return render(request, 'recipes/shopList.html', {'recipes': recipe_in_basket})


@login_required
def get_shoplist(request):
    user = request.user
    shop_list = user.shop_list.all()
    ingredients_in_basket = []
    if shop_list:
        ingredients_in_basket = RecipeIngredient.objects.filter(
            recipe_id__in=shop_list.values('recipe_id'))
    
    filename = 'shoplist {0}.txt'.format(user.username)
    content = generate_content_shoplist(ingredients_in_basket)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename={0}'.format(filename)
    )
    return response


@login_required
def favorites_view(request):
    favorites_recipe = Recipe.objects.filter(
        id__in=request.user.recipes_favorites.values(
            'recipe_id').order_by('-pub_date')
    )
    tags = get_tags(request)
    if tags:
        favorites_recipe = filtering_by_tags(favorites_recipe, tags)
    paginator = Paginator(favorites_recipe, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/favorites.html', 
                  {'page': page, 'paginator': paginator, 'tags': tags})


@login_required
def follow_view(request):
    authors = User.objects.filter(
        id__in=request.user.follower.values('author_id')
    )
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/myFollow.html', {'page': page, 'paginator': paginator})


def profile_view(request, username):
    author = get_object_or_404(User, username=username)
    recipes_list = author.author_recipes.all().order_by('-pub_date')
    tags = get_tags(request)
    if tags:
        recipes_list = filtering_by_tags(recipes_list, tags)
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/authorRecipe.html', {'page': page, 'paginator': paginator, 'tags': tags, 'author': author})

    


def page_not_found(request, exception):
    return render(request, 'tool/customPage.html',
                  {'text': 'Страница не найдена'}, status=404)


def server_error(request):
    return render(
        request, 'tool/customPage.html',
        {'text': 'Ошибка на сервере, попробуйте обновить страницу'},
        status=500)