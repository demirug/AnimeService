# Generated by Django 3.2 on 2022-06-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('content', models.TextField(verbose_name='Content')),
                ('draft', models.BooleanField(default=False, verbose_name='Состояние')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
            ],
            options={
                'verbose_name': 'Text page',
                'verbose_name_plural': 'Text pages',
            },
        ),
    ]
