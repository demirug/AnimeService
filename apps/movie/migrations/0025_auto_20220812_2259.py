# Generated by Django 3.2 on 2022-08-12 22:59

import apps.movie.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0024_auto_20220630_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='episodefile',
            name='path',
            field=models.CharField(blank=True, max_length=150, validators=[apps.movie.models.extension_validation], verbose_name='File path'),
        ),
        migrations.AlterField(
            model_name='episodefile',
            name='file',
            field=models.FileField(blank=True, upload_to=apps.movie.models.anime_path, validators=[django.core.validators.FileExtensionValidator(['webm', 'mpg', 'ogg', 'mp4', 'mpeg'])]),
        ),
    ]