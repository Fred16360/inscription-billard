# Generated by Django 3.2.6 on 2021-12-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_auto_20211215_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saison',
            name='date_debut',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='saison',
            name='date_fin',
            field=models.DateField(),
        ),
    ]
