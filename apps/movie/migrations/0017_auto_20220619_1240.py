# Generated by Django 3.2 on 2022-06-19 09:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0016_auto_20220619_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviesettings',
            name='max_rating_val',
            field=models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Maximum rating value'),
        ),
        migrations.AddField(
            model_name='moviesettings',
            name='min_rating_val',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Minimum rating value'),
        ),
    ]