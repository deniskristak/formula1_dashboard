# Generated by Django 3.2.18 on 2023-03-07 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets_dash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerpoint',
            name='points_quali',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerpoint',
            name='points_race',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerpoint',
            name='points_sprint',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='results',
            name='position',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='results',
            name='position_quali',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='results',
            name='position_sprint',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
