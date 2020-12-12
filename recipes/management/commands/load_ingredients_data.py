import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Наполнение базы данных ингредиентами'

    def handle(self, *args, **options):
        
        with open('recipes/fixtures/ingredients.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(name=name, unit=unit)
