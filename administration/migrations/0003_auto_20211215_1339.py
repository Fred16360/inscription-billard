# Generated by Django 3.2.6 on 2021-12-15 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_saison_nom_saison'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saison',
            name='date_debut',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='saison',
            name='date_fin',
            field=models.DateTimeField(),
        ),
    ]
