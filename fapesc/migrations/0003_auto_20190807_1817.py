# Generated by Django 2.2.4 on 2019-08-07 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fapesc', '0002_auto_20190807_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='comunidade',
            name='permissao',
            field=models.CharField(default='N', max_length=128),
        ),
        migrations.AddField(
            model_name='comunidade',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fapesc.usuario'),
        ),
        migrations.AlterField(
            model_name='casos',
            name='permissao',
            field=models.CharField(default='S', max_length=128),
        ),
        migrations.AlterField(
            model_name='imagem',
            name='img',
            field=models.ImageField(blank=True, upload_to='static/media/media/'),
        ),
        migrations.AlterField(
            model_name='imagem',
            name='permissao',
            field=models.CharField(default='N', max_length=128),
        ),
    ]
