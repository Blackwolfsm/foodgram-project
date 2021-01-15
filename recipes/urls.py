from django.urls import path
from django.conf.urls import handler404, handler500

from . import views


handler404 = 'recipes.views.page_not_found'
handler500 = 'recipes.views.server_error'


urlpatterns = [
    path('recipes/new', views.create_recipe, name='create_recipe'),
    path('recipes/<username>/<recipe_id>', views.recipe_view, name='recipe_view'),
    path('recipes/shoplist', views.shoplist_view, name='shoplist'),
    path('', views.index, name='index'),
]