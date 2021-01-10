from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from recipes.models import Ingredient, User, Follow
from .serializers import IngredientsSerializer


@api_view(['GET'])
def ingredient(request):
    filters = request.GET.get('query')
    ingredients = Ingredient.objects.filter(name__icontains=filters.lower())
    serializer = IngredientsSerializer(ingredients, many=True)
    return Response(serializer.data)


class Subcribe(APIView):
    
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

