# Generated by Django 2.2.4 on 2019-09-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fapesc', '0004_auto_20190807_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagem',
            name='img',
            field=models.ImageField(blank=True, upload_to='media/media/'),
        ),
    ]
