# Generated by Django 5.1.3 on 2024-11-29 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='house',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.house'),
        ),
        migrations.AlterField(
            model_name='team',
            name='players',
            field=models.ManyToManyField(related_name='teams', to='home.player'),
        ),
    ]
