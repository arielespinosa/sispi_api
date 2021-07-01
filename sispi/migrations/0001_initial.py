# Generated by Django 3.2.4 on 2021-07-01 14:41

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Municipios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4608)),
                ('municipio', models.CharField(blank=True, max_length=25, null=True)),
                ('provincia', models.CharField(blank=True, max_length=25, null=True)),
                ('area', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
            ],
            options={
                'db_table': 'municipios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug_name', models.SlugField(max_length=5)),
                ('resolution', models.IntegerField()),
                ('grid', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('model', models.CharField(blank=True, choices=[('SisPI', 'Sistema de Pronóstico Inmediato'), ('SPNOA', 'Śistema de Pronóstico Oceano-Atmosférico')], max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.PositiveSmallIntegerField(default=0)),
                ('forecast', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PointLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.SlugField(blank=True, max_length=40, null=True)),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('km2', models.FloatField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4608)),
            ],
        ),
        migrations.CreateModel(
            name='UM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug_name', models.SlugField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RunOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utc_init_date', models.DateTimeField()),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='domain', to='sispi.domain')),
                ('forecast', models.ManyToManyField(blank=True, null=True, related_name='outputs', to='sispi.Forecast')),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('km2', models.FloatField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4608)),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sispi.province')),
            ],
        ),
        migrations.CreateModel(
            name='MetVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('um', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sispi.um')),
            ],
        ),
        migrations.CreateModel(
            name='Historical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('municipality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sispi.municipality')),
            ],
        ),
        migrations.AddField(
            model_name='domain',
            name='points',
            field=models.ManyToManyField(related_name='domain', to='sispi.PointLocation'),
        ),
    ]