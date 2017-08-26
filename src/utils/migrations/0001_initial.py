# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 16:28
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings

from utils.models import Departamento, Provincia


class Migration(migrations.Migration):

    initial = True

    dependencies = [

    ]

    operations = [
        migrations.CreateModel(
            name='Tiposdocumentos',
            fields=[
                ('activo', models.BooleanField(default=True)),
                ('id_tipo', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=25, null=True)),
            ],
            options={
                'db_table': 'tipo_documento',
                'managed': settings.IS_TESTING,
            },
        ),
        migrations.CreateModel(
            name='TipoSexo',
            fields=[
                ('activo', models.BooleanField()),
                ('id_sexo', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'tipo_sexo',
                'managed': settings.IS_TESTING,
            },
        ),
        migrations.CreateModel(
            name='TiposGrados',
            fields=[
                ('activo', models.BooleanField()),
                ('id_tipo_grado', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tipos_grados',
                'managed': settings.IS_TESTING,
            },
        ),
        migrations.CreateModel(
            name='TiposMedioPago',
            fields=[
                ('activo', models.BooleanField()),
                ('id_tipo_medio', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'tipos_medio_pago',
                'managed': settings.IS_TESTING,
            },
        ),
        migrations.CreateModel(
            name='TiposNivel',
            fields=[
                ('activo', models.BooleanField()),
                ('id_tipo', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'tipos_nivel',
                'managed': settings.IS_TESTING,
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('activo', models.BooleanField()),
                ('id_departamento', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'departamennto',
                'managed': settings.IS_TESTING,
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('activo', models.BooleanField()),
                ('id_provincia', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('id_departamento', models.ForeignKey(db_column='id_departamento', to='utils.Departamento', null=True)),

            ],
            options={
                'db_table': 'provincia',
                'managed': settings.IS_TESTING,
            },
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('activo', models.BooleanField()),
                ('id_distrito', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200)),
                ('id_provincia', models.ForeignKey(db_column='id_provincia', to='utils.Provincia', null=True)),

            ],
            options={
                'db_table': 'distrito',
                'managed': settings.IS_TESTING,
            },
        ),
    ]
