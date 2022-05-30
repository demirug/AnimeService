# Generated by Django 3.2 on 2022-05-29 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0003_auto_20220525_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Review')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('verified', models.BooleanField(default=False)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movie.season')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'unique_together': {('season', 'user')},
            },
        ),
    ]