# Generated by Django 3.2.18 on 2023-02-26 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('default_position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('country', models.CharField(max_length=300)),
                ('is_sprint', models.BooleanField(default=False)),
                ('datetime_of_race_gmt', models.DateTimeField()),
            ],
            options={
                'ordering': ['datetime_of_race_gmt'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='RaceTip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField()),
                ('position_quali', models.PositiveSmallIntegerField()),
                ('fastest_lap', models.BooleanField(default=False)),
                ('dotd', models.BooleanField(default=False)),
                ('dnf', models.BooleanField(default=False)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tips_input.driver')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tips_input.player')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tips_input.race')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='driver',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tips_input.team'),
        ),
    ]
