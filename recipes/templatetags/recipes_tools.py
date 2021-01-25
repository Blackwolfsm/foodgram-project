from django import template

register = template.Library()


@register.filter
def is_favorites(user, recipe_id):
    """
    Фильтр проверяет, есть ли у user в избранном рецепт с id который передан
    в recipe_id.
    """
    check = user.recipes_favorites.filter(recipe_id=recipe_id).exists()
    return check


@register.filter
def is_follower(user, author_id):
    """
    Фильтр проверяет, есть ли у user подписка на автора с id который передан
    в author_id.
    """
    check = user.follower.filter(author_id=author_id).exists()
    return check


@register.filter
def count_purchases(user):
    """Фильтр подсчитывает кол-во рецептов в корзине у пользователя."""
    count = user.shop_list.all().count()
    return count


@register.filter
def recipe_in_basket(user, recipe_id):
    """Фильтр проверяет, есть ли рецепт с id в корзине покупателя."""
    check = user.shop_list.filter(recipe_id=recipe_id).exists()
    return check


@register.filter
def formating_tags(request, tag):
    if 'tags' in request.GET:

        tags = request.GET.get('tags')
        tags = tags.split(',')

        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
        if '' in tags:
            tags.remove('')

        result = ','.join(tags)
        return result
    
    return tag


@register.filter
def count_text_for_myfollow(queryset):
    text = 'Еще '
    count = queryset.count() - 3
    if count == 1:
        text += '1 рецепт'
    elif count < 5:
        text += f'{count} рецепта'
    else:
        text += f'{count} рецептов'
    return text