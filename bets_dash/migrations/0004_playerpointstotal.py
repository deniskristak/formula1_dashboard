# Generated by Django 3.2.18 on 2023-03-07 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bets_input', '0004_auto_20230306_0059'),
        ('bets_dash', '0003_auto_20230306_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerPointsTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points_total', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bets_input.player')),
            ],
        ),
    ]
