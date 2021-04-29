# Generated by Django 2.2.5 on 2021-04-19 14:35

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sispi', '0002_remove_pointlocation_ref'),
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
    ]
