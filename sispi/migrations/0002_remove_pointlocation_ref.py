# Generated by Django 2.2.5 on 2021-04-17 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sispi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointlocation',
            name='ref',
        ),
    ]