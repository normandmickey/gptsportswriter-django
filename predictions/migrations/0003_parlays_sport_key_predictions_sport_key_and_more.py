# Generated by Django 5.0.6 on 2025-05-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0002_alter_parlays_slug_alter_predictions_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parlays',
            name='sport_key',
            field=models.TextField(default='baseball_mlb'),
        ),
        migrations.AddField(
            model_name='predictions',
            name='sport_key',
            field=models.TextField(default='baseball_mlb'),
        ),
        migrations.AddField(
            model_name='props',
            name='sport_key',
            field=models.TextField(default='baseball_mlb'),
        ),
        migrations.AddField(
            model_name='recaps',
            name='sport_key',
            field=models.TextField(default='baseball_mlb'),
        ),
    ]
