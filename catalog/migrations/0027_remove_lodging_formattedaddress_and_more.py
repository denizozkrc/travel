# Generated by Django 5.0.7 on 2024-08-27 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_lodging_formattedaddress_lodging_location_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lodging',
            name='formattedAddress',
        ),
        migrations.RemoveField(
            model_name='lodging',
            name='location_id',
        ),
        migrations.RemoveField(
            model_name='lodging',
            name='location_name',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='formattedAddress',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='location_id',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='location_name',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='formattedAddress',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='location_id',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='location_name',
        ),
    ]
