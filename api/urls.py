from django.urls import path
from rest_framework.authtoken import views as authviews

from . import views


urlpatterns = [
    path('ingredients/', views.ingredient, name='ingredients'),
    path('follow', views.Subcribe.as_view(), name='profile_follow'),
]


urlpatterns += [
    path('api-token-auth/', authviews.obtain_auth_token),
]