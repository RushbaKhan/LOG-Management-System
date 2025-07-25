# Generated by Django 5.1.3 on 2024-11-15 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.AutoField(primary_key=True, serialize=False)),
                ('game_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('house_id', models.AutoField(primary_key=True, serialize=False)),
                ('house_name', models.CharField(max_length=100, unique=True)),
                ('captain_id', models.IntegerField()),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.AutoField(primary_key=True, serialize=False)),
                ('game_id', models.IntegerField()),
                ('venue_id', models.IntegerField()),
                ('scheduled_date', models.DateField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('venue_id', models.AutoField(primary_key=True, serialize=False)),
                ('venue_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GameRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.TextField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.game')),
            ],
        ),
        migrations.CreateModel(
            name='MatchHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.house')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.match')),
            ],
        ),
        migrations.CreateModel(
            name='MatchResult',
            fields=[
                ('result_id', models.AutoField(primary_key=True, serialize=False)),
                ('scores', models.CharField(max_length=100)),
                ('winner', models.CharField(max_length=100)),
                ('match', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.match')),
            ],
        ),
        migrations.CreateModel(
            name='MatchStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.house')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.match')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=50)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.house')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('fouls', models.IntegerField()),
                ('yellow_cards', models.IntegerField()),
                ('red_cards', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.player')),
            ],
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('rank_id', models.AutoField(primary_key=True, serialize=False)),
                ('points', models.IntegerField()),
                ('position', models.IntegerField()),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.house')),
            ],
        ),
        migrations.CreateModel(
            name='MatchSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_date', models.DateField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.match')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.venue')),
            ],
        ),
    ]
