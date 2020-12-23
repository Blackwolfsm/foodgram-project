from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Ingredient
from .serializers import IngredientsSerializer


@api_view(['GET'])
def ingredient(request):
    filters = request.GET.get('query')
    ingredients = Ingredient.objects.filter(name__icontains=filters)
    serializer = IngredientsSerializer(ingredients, many=True)
    return Response(serializer.data)
