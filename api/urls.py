from django.urls import path

from . import views


urlpatterns = [
    path('ingredients/', views.ingredient, name='ingredients')
]