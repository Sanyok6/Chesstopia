# Generated by Django 4.0.6 on 2022-07-27 06:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0004_alter_chessmatch_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessmatch',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
