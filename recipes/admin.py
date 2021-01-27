from django.contrib import admin

from recipes.models import (Follow, Ingredient, Recipe, RecipeFavorites,
                            RecipeIngredient, ShoppingList)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_filter = ('title',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)


admin.site.register(RecipeIngredient)
admin.site.register(Follow)
admin.site.register(RecipeFavorites)
admin.site.register(ShoppingList)
