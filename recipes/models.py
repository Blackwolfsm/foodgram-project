from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента',
                            max_length=256)
    unit = models.CharField('Ед. измерения',
                            max_length=64)

    def __str__(self):
        return f'{self.name} ({self.unit})'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_recipes')
    title = models.CharField('Название рецепта', max_length=256)
    descriptions = models.TextField('Описание рецепта', max_length=1024)
    cooking_time = models.IntegerField('Время приготовления в минутах')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient')
    breakfast = models.BooleanField('Завтрак', default=False)
    lunch = models.BooleanField('Обед', default=False)
    dinner = models.BooleanField('Ужин', default=False)
    image = models.ImageField('Картинка для рецепта', upload_to='recipes/')
    pub_date = models.DateTimeField(verbose_name='Дата добавления рецепта',
                                    auto_now_add=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField('Количество')


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    def __str__(self):
        return f'Подписка пользователя {self.user} на автора {self.author}'


class RecipeFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='recipes_favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='in_fovorites')


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shop_list')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
