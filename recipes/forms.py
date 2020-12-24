from django.forms import ModelForm
from django import forms

from .models import Recipe


def set_field_html_name(cls, new_name):
       """
       This creates wrapper around the normal widget rendering, 
       allowing for a custom field name (new_name).
       """
       old_render = cls.widget.render
       def _widget_render_wrapper(name, value, attrs=None):
           return old_render(new_name, value, attrs)

       cls.widget.render = _widget_render_wrapper

class RecipeForm(forms.Form):
    title = forms.CharField()
    descriptions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form__input'}))
    cooking_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form__input'}))
    set_field_html_name(title, 'name')


# class RecipeForm(ModelForm):
#     class Meta:
#         model = Recipe
#         fields = ['title', 'ingredients', 'descriptions', 'cooking_time']
#         widgets = {
#             'title': forms.TextInput(attrs={'name': 'name'}),
#             'descriptions': forms.Textarea(attrs={'name': 'description'}),
#             'cooking_time': forms.NumberInput(attrs={'name': 'time'}),
#         }

