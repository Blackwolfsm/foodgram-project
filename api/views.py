from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
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


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def profile_follow(request):
    print(request.POST)
    print('привет')
    return Response('Ghbdtn')

class Subcribe(APIView):
    def post(self, request):
        author_recipe = User.objects.get(id=request.data['id'])
        user = request.user
        check_have_sub = user.follower.filter(author=author_recipe).exists()
        if not check_have_sub and author_recipe != user:
            Follow.objects.create(author=author_recipe, user=user)
            return Response({'success': 'True'}, status=status.HTTP_201_CREATED)
        return Response({'succes': 'False'}, status=status.HTTP_400_BAD_REQUEST)
