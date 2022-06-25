# Generated by Django 3.2 on 2022-06-25 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textpage', '0002_alter_textpage_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='textpage',
            name='content_en',
            field=models.TextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='textpage',
            name='content_uk',
            field=models.TextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='textpage',
            name='name_en',
            field=models.CharField(max_length=150, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='textpage',
            name='name_uk',
            field=models.CharField(max_length=150, null=True, verbose_name='Name'),
        ),
    ]
