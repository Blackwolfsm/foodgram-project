from django import template

from recipes.models import RecipeFavorites


register = template.Library()


@register.filter
def is_favorites(user, recipe_id):
    """Фильтр проверяет, есть ли у user в избранном рецепт с id который передан
    в recipe_id.
    """
    check = user.recipes_favorites.filter(recipe_id=recipe_id).exists()
    return check


@register.filter
def is_follower(user, author_id):
    """Фильтр проверяет, есть ли у user подписка на автора с id который передан
    в author_id.
    """
    check = user.follower.filter(author_id=author_id).exists()
    return check