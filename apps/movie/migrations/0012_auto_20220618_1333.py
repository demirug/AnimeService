# Generated by Django 3.2 on 2022-06-18 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0011_auto_20220615_1254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ratingstar',
            options={'ordering': ['value'], 'verbose_name': 'Rating Star', 'verbose_name_plural': 'Rating Stars'},
        ),
        migrations.AlterField(
            model_name='ratingstar',
            name='value',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
    ]
