

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
    print(data)

    return data