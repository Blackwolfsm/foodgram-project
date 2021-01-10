from django.urls import path

from . import views


urlpatterns = [
    path('recipes/new', views.create_recipe, name='create_recipe'),
    path('recipes/<username>/<recipe_id>', views.recipe_view, name='recipe_view'),
    path('', views.index, name='index'),
]