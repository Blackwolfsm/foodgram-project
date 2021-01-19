from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from recipes.models import (Ingredient, User, Follow, Recipe,
                            RecipeFavorites, ShoppingList)
from .serializers import IngredientsSerializer


@api_view(['GET'])
def ingredient(request):
    filters = request.GET.get('query')
    ingredients = Ingredient.objects.filter(name__icontains=filters.lower())
    serializer = IngredientsSerializer(ingredients, many=True)
    return Response(serializer.data)


class Subcribe(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        author_recipe = User.objects.get(id=request.data['id'])
        user = request.user
        check_have_sub = user.follower.filter(author=author_recipe).exists()
        if not check_have_sub and author_recipe != user:
            Follow.objects.create(author=author_recipe, user=user)
            return Response({'success': 'True'}, status=status.HTTP_201_CREATED)
        return Response({'succes': 'False'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        author_recipe = User.objects.get(id=request.data['id'])
        user = request.user
        subcribe = user.follower.filter(author=author_recipe)
        if subcribe:
            user.follower.get(author=author_recipe).delete()
            return Response({'success': 'True'}, status=status.HTTP_200_OK)
        return Response({'succes': 'False'}, status=status.HTTP_400_BAD_REQUEST)

class Favorites(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        user = request.user
        check_in_fav = user.recipes_favorites.filter(recipe_id=recipe.id).exists()
        if check_in_fav:
            return Response({'succes': 'False'}, status=status.HTTP_400_BAD_REQUEST)
        RecipeFavorites.objects.create(recipe=recipe,user=user)
        return Response({'success': 'True'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        user = request.user
        recipe_in_fav = user.recipes_favorites.filter(recipe_id=recipe.id)
        if recipe_in_fav:
            user.recipes_favorites.get(recipe_id=recipe.id).delete()
            return Response({'success': 'True'}, status=status.HTTP_200_OK)
        return Response({'succes': 'False'}, status=status.HTTP_400_BAD_REQUEST)


class Purchase(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        user = request.user
        recipe_in_basket = user.shop_list.filter(recipe_id=recipe.id).exists()
        if recipe_in_basket:
            return Response({'succes': 'False'}, status=status.HTTP_400_BAD_REQUEST)
        ShoppingList.objects.create(user=user, recipe=recipe)
        return Response({'success': 'True'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        recipe = Recipe.objects.get(id=request.data['id'])
        user = request.user
        recipe_in_basket = user.shop_list.filter(recipe_id=recipe.id).exists()
        if recipe_in_basket:
            user.shop_list.get(recipe_id=recipe.id).delete()
            return Response({'success': 'True'}, status=status.HTTP_200_OK)
        return Response({'succes': 'False'}, status=status.HTTP_400_BAD_REQUEST)
