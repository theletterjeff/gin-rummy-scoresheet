# Generated by Django 4.0.3 on 2022-05-08 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_playerprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='playerprofile',
            options={'ordering': ['pk']},
        ),
    ]
