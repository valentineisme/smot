# Generated by Django 2.2.4 on 2019-09-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fapesc', '0007_auto_20190903_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagem',
            name='img',
            field=models.ImageField(blank=True, upload_to='home/aluno'),
        ),
    ]