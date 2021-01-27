from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (Follow, Ingredient, Recipe, RecipeFavorites,
                            ShoppingList, User)

from .serializers import IngredientsSerializer


@api_view(['GET'])
def ingredient(request):
    filters = request.GET.get('query')
    if filters:
        ingredients = Ingredient.objects.filter(
            name__icontains=filters.lower())
        serializer = IngredientsSerializer(ingredients, many=True)
        return Response(serializer.data)
    return Response({'success': 'False'}, status=status.HTTP_400_BAD_REQUEST)


class Subcribe(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        author_recipe = get_object_or_404(User, id=request.data['id'])
        user = request.user
        check_have_sub = user.follower.filter(author=author_recipe).exists()
        if not check_have_sub and author_recipe != user:
            Follow.objects.create(author=author_recipe, user=user)
            return Response({'success': 'True'},
                            status=status.HTTP_201_CREATED)
        return Response({'success': 'False'},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        author_recipe = get_object_or_404(User, id=request.data['id'])
        user = request.user
        subscribe = get_object_or_404(Follow, user=user, author=author_recipe)
        subscribe.delete()
        return Response({'success': 'True'}, status=status.HTTP_200_OK)


class Favorites(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipe = get_object_or_404(Recipe, id=request.data['id'])
        user = request.user
        check_in_fav = user.recipes_favorites.filter(
            recipe_id=recipe.id).exists()
        if not check_in_fav:
            RecipeFavorites.objects.create(recipe=recipe, user=user)
            return Response({'success': 'True'},
                            status=status.HTTP_201_CREATED)
        return Response({'success': 'False'},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        recipe = get_object_or_404(Recipe, id=request.data['id'])
        user = request.user
        recipe_in_fav = get_object_or_404(RecipeFavorites,
                                          recipe=recipe, user=user)
        recipe_in_fav.delete()
        return Response({'success': 'True'}, status=status.HTTP_200_OK)


class Purchase(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipe = get_object_or_404(Recipe, id=request.data['id'])
        user = request.user
        recipe_in_basket = user.shop_list.filter(recipe_id=recipe.id).exists()
        if not recipe_in_basket:
            ShoppingList.objects.create(user=user, recipe=recipe)
            return Response({'success': 'True'},
                            status=status.HTTP_200_OK)
        return Response({'succes': 'False'},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        recipe = get_object_or_404(Recipe, id=request.data['id'])
        user = request.user
        recipe_in_basket = get_object_or_404(ShoppingList,
                                             recipe=recipe, user=user)
        recipe_in_basket.delete()
        return Response({'success': 'True'}, status=status.HTTP_200_OK)
