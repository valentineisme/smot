# Generated by Django 2.2.4 on 2019-09-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fapesc', '0013_auto_20190930_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagem',
            name='img',
            field=models.ImageField(blank=True, upload_to='static/media/media/ %}'),
        ),
    ]