# Generated by Django 3.1.4 on 2021-01-27 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20210127_1505'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='descriptions',
            new_name='description',
        ),
    ]