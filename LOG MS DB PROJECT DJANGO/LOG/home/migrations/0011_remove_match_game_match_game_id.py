# Generated by Django 5.1.3 on 2024-11-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_rename_game_id_match_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='game',
        ),
        migrations.AddField(
            model_name='match',
            name='game_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
