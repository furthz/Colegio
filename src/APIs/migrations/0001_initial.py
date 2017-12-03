# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 20:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
                     ('profile','0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoAlerta',
            fields=[
                ('id_estado_alerta', models.AutoField(primary_key=True)),
                ('nombre', models.CharField(max_length=100, blank=True, null=True)),

            ],
            options={
                #'db_table': 'tipo_servicio',
                'managed': settings.IS_MIGRATE,
                #'managed': False,

            },
        ),
        migrations.CreateModel(
            name='TipoAlerta',
            fields=[
                ('id_tipo_alerta', models.AutoField(primary_key=True)),
                ('nombre', models.CharField(max_length=100, blank=True, null=True)),
            ],
            options={
                #'db_table': 'servicio',
                'managed': settings.IS_MIGRATE,
                #'managed': False,

            },
        ),
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id_alerta', models.AutoField(primary_key=True)),
                ('persona_receptor', models.ForeignKey(db_column="id_persona", to='profiles.Profile')),
                ('curso', models.ForeignKey(db_column="id_curso", to='AE_academico.Curso')),
                ('tipo_alerta', models.ForeignKey(db_column="id_tipo_alerta", to='APIs.TipoAlerta')),
                ('estado_alerta', models.IntegerField()),
                ('estado_visto', models.BooleanField(default=False)),
                ('descripcion', models.CharField(max_length=300)),
                ('fecha_visto', models.DateTimeField(null=True, blank=True)),
                ('fecha_programada', models.DateTimeField(null=True, blank=True)),
                ('fecha_recibido', models.DateTimeField(null=True, blank=True)),
                ('fecha_creacion', models.DateField()),
                ('fecha_modificacion', models.DateField()),
                ('usuario_creacion', models.CharField(max_length=10, null=True)),
                ('usuario_modificacion', models.CharField(max_length=10, null=True)),
                ('activo', models.BooleanField()),
            ],
            options={
                # 'db_table': 'matricula',
                'managed': settings.IS_MIGRATE,
                # 'managed': False,

            },
        ),
    ]

