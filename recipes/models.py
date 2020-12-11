from django.db import models


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента',
                            max_length=256)
    unit = models.CharField('Ед. измерения',
                            max_length=64)

    def __str__(self):
        return f'{self.name} ({self.unit})'