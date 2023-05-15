# Generated by Django 3.2.19 on 2023-05-15 20:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book_club', '0003_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
