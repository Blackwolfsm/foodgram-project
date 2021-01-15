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