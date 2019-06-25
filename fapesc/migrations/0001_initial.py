# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-06-05 17:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='casos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distancia', models.IntegerField(default=0)),
                ('resultado', models.CharField(max_length=128)),
                ('plano_acao', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Caso',
                'verbose_name_plural': 'Casos',
            },
        ),
        migrations.CreateModel(
            name='comunidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
                ('bairro', models.CharField(max_length=128)),
                ('cidade', models.CharField(max_length=128)),
                ('estado', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Comunidade',
                'verbose_name_plural': 'Comunidades',
            },
        ),
        migrations.CreateModel(
            name='historico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True)),
                ('objeto1', models.CharField(max_length=128)),
                ('relacao', models.CharField(max_length=128)),
                ('objeto2', models.CharField(max_length=128)),
                ('distancia', models.IntegerField(default=0)),
                ('resultado', models.CharField(max_length=128)),
                ('plano_acao', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Historico',
                'verbose_name_plural': 'Historico',
            },
        ),
        migrations.CreateModel(
            name='imagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to=b'static/media/media/')),
                ('dataImagem', models.DateField(blank=True)),
                ('latitude', models.CharField(max_length=128)),
                ('longitude', models.CharField(max_length=128)),
                ('comunidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapesc.comunidade')),
            ],
            options={
                'verbose_name': 'Imagem',
                'verbose_name_plural': 'Imagens',
            },
        ),
        migrations.CreateModel(
            name='objeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Objeto',
                'verbose_name_plural': 'Objetos',
            },
        ),
        migrations.CreateModel(
            name='relacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Relacao',
                'verbose_name_plural': 'Relacoes',
            },
        ),
        migrations.CreateModel(
            name='restricao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=128)),
                ('distancia', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Restricao',
                'verbose_name_plural': 'Restricoes',
            },
        ),
        migrations.CreateModel(
            name='usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
                ('sobrenome', models.CharField(max_length=128)),
                ('dataNasc', models.DateField(blank=True, null=True)),
                ('email', models.CharField(max_length=128)),
                ('senha', models.CharField(max_length=128, null=True)),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.AddField(
            model_name='imagem',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapesc.usuario'),
        ),
        migrations.AddField(
            model_name='historico',
            name='imagem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fapesc.imagem'),
        ),
        migrations.AddField(
            model_name='historico',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapesc.usuario'),
        ),
        migrations.AddField(
            model_name='casos',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapesc.usuario'),
        ),
        migrations.AddField(
            model_name='casos',
            name='objeto1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objeto1', to='fapesc.objeto'),
        ),
        migrations.AddField(
            model_name='casos',
            name='objeto2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objeto2', to='fapesc.objeto'),
        ),
        migrations.AddField(
            model_name='casos',
            name='relacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapesc.relacao'),
        ),
        migrations.AddField(
            model_name='casos',
            name='restricao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fapesc.restricao'),
        ),
    ]
