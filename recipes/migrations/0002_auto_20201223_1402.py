# Generated by Django 3.1.4 on 2020-12-23 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='breakfast',
            field=models.BooleanField(default=False, verbose_name='Завтрак'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='dinner',
            field=models.BooleanField(default=False, verbose_name='Обед'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='NULL', null=True, upload_to='', verbose_name='Картинка для рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='lunch',
            field=models.BooleanField(default=False, verbose_name='Ужин'),
        ),
    ]
