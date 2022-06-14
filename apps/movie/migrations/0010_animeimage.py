# Generated by Django 3.2 on 2022-06-14 17:00

import apps.movie.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0009_auto_20220613_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to=apps.movie.models.anime_image_path)),
                ('wight', models.SmallIntegerField(default=0)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='movie.season')),
            ],
            options={
                'verbose_name': 'AnimeImage',
                'verbose_name_plural': 'AnimeImages',
                'ordering': ['wight'],
            },
        ),
    ]
