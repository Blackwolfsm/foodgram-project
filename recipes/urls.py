from django.urls import path

from . import views

urlpatterns = [
    path('recipes/new', views.create_recipe, name='create_recipe'),
    path('recipes/shoplist', views.shoplist_view, name='shoplist'),
    path('recipes/get_shoplist', views.get_shoplist, name='get_shoplist'),
    path('recipes/favorites', views.favorites_view, name='favorites'),
    path('recipes/follow', views.follow_view, name='follow'),
    path('recipes/<username>', views.profile_view, name='profile'),
    path('recipes/<username>/<recipe_id>', views.recipe_view, name='recipe_view'),
    path('recipes/<username>/<recipe_id>/edit', views.edit_recipe, name='edit_recipe'),
    path('', views.index, name='index'),
]
