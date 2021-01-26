from django.urls import path

from . import views

urlpatterns = [
    path('ingredients/', views.ingredient, name='ingredients'),
    path('follow/', views.Subcribe.as_view(), name='profile_follow'),
    path('favorites/', views.Favorites.as_view(), name='favorites_recipes'),
    path('purchases/', views.Purchase.as_view(), name='purchases'),
]
