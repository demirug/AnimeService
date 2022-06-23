# Generated by Django 3.2 on 2022-06-23 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0002_rename_question_feedback'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DefaultAnswer',
            new_name='FAQ',
        ),
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQ'},
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ['answered'], 'verbose_name': 'Feedback', 'verbose_name_plural': 'Feedbacks'},
        ),
    ]
