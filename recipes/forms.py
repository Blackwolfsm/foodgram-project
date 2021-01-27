from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Ingredient, Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'breakfast', 'dinner', 'lunch',
                  'cooking_time', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form__input', 'id': 'id_name'})
        self.fields['breakfast'].widget.attrs.update(
            {'class': 'tags__checkbox tags__checkbox_style_orange'})
        self.fields['lunch'].widget.attrs.update(
            {'class': 'tags__checkbox tags__checkbox_style_green'})
        self.fields['dinner'].widget.attrs.update(
            {'class': 'tags__checkbox tags__checkbox_style_purple'})
        self.fields['cooking_time'].widget.attrs.update(
            {'class': 'form__input', 'id': 'id_time', })
        self.fields['cooking_time'].widget.attrs['min'] = 1
        self.fields['description'].widget.attrs.update(
            {'rows': 8, 'class': 'form__textarea', 'id': 'id_description'})
        self.fields['image'].widget.attrs.update({'id': 'id_file'})

    def clean(self):
        cleaned_data = super().clean()
        breakfast = cleaned_data.get('breakfast')
        dinner = cleaned_data.get('dinner')
        lunch = cleaned_data.get('lunch')

        if not breakfast and not dinner and not lunch:
            self.add_error(
                'breakfast',
                ValidationError('Вы должны указать хотя бы один тэг')
            )

        one_or_more = False
        for key in self.data.keys():
            if key.startswith('nameIngredient_'):
                check_in_bd = Ingredient.objects.filter(name=self.data[key])
                if not check_in_bd:
                    raise ValidationError('Передан не допустимый ингредиент',
                                          code='ingredient')
                one_or_more = True
        if not one_or_more:
            raise ValidationError('Добавьте хотя бы один ингредиент',
                                  code='ingredient')
