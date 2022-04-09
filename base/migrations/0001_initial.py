# Generated by Django 4.0.3 on 2022-04-02 19:27

import base.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_started', models.DateTimeField(auto_now_add=True)),
                ('datetime_ended', models.DateTimeField(blank=True, null=True)),
                ('target_score', models.IntegerField(default=500, validators=[base.validators.validate_gt_zero])),
                ('players', models.ManyToManyField(related_name='matches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(validators=[base.validators.validate_gt_zero])),
                ('gin', models.BooleanField(default=False)),
                ('undercut', models.BooleanField(default=False)),
                ('datetime_played', models.DateTimeField(auto_now_add=True)),
                ('loser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_losses', to=settings.AUTH_USER_MODEL)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.match')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_wins', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_score', models.IntegerField(default=0)),
                ('match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.match')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'unique_together': {('match', 'player')},
            },
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.BooleanField(default=False)),
                ('player_outcome', models.IntegerField(blank=True, choices=[(1, 'Win'), (0, 'Loss')], null=True)),
                ('match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.match')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'unique_together': {('match', 'player')},
            },
        ),
    ]