# Generated by Django 3.2 on 2022-06-24 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0004_remove_faq_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='answer',
            field=models.TextField(blank=True, verbose_name='Answer'),
        ),
    ]
