# Generated by Django 3.2 on 2022-06-25 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0005_alter_feedback_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='answer_en',
            field=models.TextField(null=True, verbose_name='Answer'),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_uk',
            field=models.TextField(null=True, verbose_name='Answer'),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_en',
            field=models.CharField(max_length=300, null=True, verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_uk',
            field=models.CharField(max_length=300, null=True, verbose_name='Question'),
        ),
    ]
