from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента',
                            max_length=256)
    unit = models.CharField('Ед. измерения',
                            max_length=64)

    def __str__(self):
        return f'{self.name} ({self.unit})'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Название рецепта', max_length=256)
    descriptions = models.TextField('Описание рецепта', max_length=1024)
    cooking_time= models.IntegerField('Время приготовления в минутах')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient')
    
    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField('Количество')