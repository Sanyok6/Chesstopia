# Generated by Django 4.0.6 on 2022-07-31 15:28

import chess.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0006_chessmatch_starting_pos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chessmatch',
            name='starting_pos',
            field=models.TextField(default=chess.models.generate_fen),
        ),
    ]