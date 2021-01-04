import re


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