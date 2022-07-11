# Generated by Django 3.2 on 2022-06-30 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0021_anime_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviesettings',
            name='new_episode_email',
            field=models.TextField(default='New episode for {name} at our site, Click to watch {url}', verbose_name='New episode email'),
        ),
    ]