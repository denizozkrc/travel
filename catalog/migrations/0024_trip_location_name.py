# Generated by Django 5.0.7 on 2024-08-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_trip_lng_trip_ltd'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='location_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
