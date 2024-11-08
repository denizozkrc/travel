# Generated by Django 5.0.7 on 2024-08-27 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_trip_formattedaddress_trip_location_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='lodging',
            name='formattedAddress',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='lodging',
            name='location_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='lodging',
            name='location_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='formattedAddress',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='location_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='location_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transport',
            name='formattedAddress',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transport',
            name='location_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transport',
            name='location_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
