# Generated by Django 3.2 on 2022-06-06 11:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0007_subscribe'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subscribe',
            unique_together={('anime', 'user')},
        ),
    ]
