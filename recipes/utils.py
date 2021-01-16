import re

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table


def parse_name_amount_ingredients(data):
    """Принимает на вход словарь, находит id ингредиентов,
       возвращает список из списков названий игредиентов с 
       количеством
    """
    list_id = []
    ing_value = []
    for key in data.keys():
        if re.match('nameIngredient_', key):
            list_id.append(key[-1])
    for index in list_id:
        name_id = 'nameIngredient_' + str(index)
        value_id = 'valueIngredient_' + str(index)
        ing_value.append([data[name_id], data[value_id]])
    return ing_value


def sum_ingredients(ingredients_with_amount):
    unique = {}
    for ingredient in ingredients_with_amount:
        if ingredient.ingredient.id not in unique:
            unique[ingredient.ingredient_id] = [
                ingredient.ingredient.name,
                ingredient.ingredient.unit,
                ingredient.amount
                ]
        else:
            unique[ingredient.ingredient_id][2] += ingredient.amount
    return unique


def generate_content_shoplist(queryset):
    ingredients = sum_ingredients(queryset)
    text = str()
    for items in ingredients.values():
        text += f'[]  {items[0]} - {items[2]} ({(items[1])}). \n'
    return text