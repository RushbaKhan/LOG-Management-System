# Generated by Django 5.1.3 on 2024-11-28 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_remove_match_game_id_match_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='venue_id',
        ),
        migrations.AddField(
            model_name='match',
            name='venue',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.venue'),
        ),
    ]
