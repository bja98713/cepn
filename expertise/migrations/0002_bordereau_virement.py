# Generated by Django 5.1.6 on 2025-04-07 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expertise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bordereau',
            name='virement',
            field=models.BooleanField(default=False, verbose_name='Virement effectué ?'),
        ),
    ]
