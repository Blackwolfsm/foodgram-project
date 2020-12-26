import re


def parse_data_for_recipe(dict_from_request):
    data = {
        'title': dict_from_request['name'],
        'descriptions': dict_from_request['description'],
        'cooking_time': dict_from_request['time'],
    }
    if 'breakfast' in dict_from_request:
        data['breakfast'] = True
    else:
        data['breakfast'] = False
    if 'lunch' in dict_from_request:
        data['lunch'] = True
    else:
        data['lunch'] = False
    if 'dinner' in dict_from_request:
        data['dinner'] = True
    else:
        data['dinner'] = False
    return data


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