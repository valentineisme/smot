# Generated by Django 2.2.4 on 2019-09-30 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fapesc', '0016_auto_20190930_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='historico',
            name='dataImagem',
            field=models.DateField(blank=True, null=True),
        ),
    ]
