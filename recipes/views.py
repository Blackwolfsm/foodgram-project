from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Recipe, Ingredient, User, RecipeIngredient, Follow, RecipeFavorites, ShoppingList
from .forms import RecipeForm
from .utils import parse_name_amount_ingredients, generate_content_shoplist


def index(request):
    recipes_list = Recipe.objects.all()
    paginator = Paginator(recipes_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', 
                  {'page': page, 'paginator': paginator})


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
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
    


def page_not_found(request, exception):
    return render(request, 'customPage.html',
                  {'text': 'Страница не найдена'}, status=404)


def server_error(request):
    return render(
        request, 'customPage.html',
        {'text': 'Ошибка на сервере, попробуйте обновить страницу'},
        status=500)