# Generated by Django 3.2.6 on 2021-12-13 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='saison',
            name='nom_saison',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
