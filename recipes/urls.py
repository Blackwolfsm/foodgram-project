from django.urls import path

from . import views


urlpatterns = [
    path('recipes/new', views.create_recipe, name='create_recipe'),
    path('', views.index, name='index'),
]