from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название ингредиента',
                            max_length=256)
    unit = models.CharField(verbose_name='Ед. измерения',
                            max_length=64)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.unit})'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_recipes',
                               verbose_name='Автор')
    title = models.CharField(verbose_name='Название рецепта', max_length=256)
    description = models.TextField(verbose_name='Описание рецепта',
                                   max_length=1024)
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингредиенты',
                                         through='RecipeIngredient')
    breakfast = models.BooleanField(verbose_name='Завтрак', default=False)
    lunch = models.BooleanField(verbose_name='Обед', default=False)
    dinner = models.BooleanField(verbose_name='Ужин', default=False)
    image = models.ImageField(verbose_name='Картинка для рецепта',
                              upload_to='recipes/')
    pub_date = models.DateTimeField(verbose_name='Дата добавления рецепта',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент')
    amount = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Пользователь')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscribe')
        ]

    def __str__(self):
        return f'Подписка пользователя {self.user} на автора {self.author}'


class RecipeFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='recipes_favorites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='in_fovorites',
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shop_list',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user}'
