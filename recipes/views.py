from django.shortcuts import render

from .models import Recipe


def index(request):
    recipes_list = Recipe.objects.all()
    return render(request, 'index.html', 
                  {'recipes_list': recipes_list})