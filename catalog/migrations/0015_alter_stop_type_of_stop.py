# Generated by Django 5.0.7 on 2024-08-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_alter_stop_type_of_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='type_of_stop',
            field=models.CharField(choices=[('sea', 'Sea'), ('cafe', 'Cafe'), ('city', 'City'), ('restaurant', 'Restaurant'), ('nature', 'Nature'), ('sightSeeing', 'Sight Seeing'), ('travel', 'Travel'), ('freeTime', 'Free Time'), ('historical_museum', 'Historical/Museum'), ('shopping', 'Shopping'), ('event', 'Event')], default='other', max_length=30),
        ),
    ]
