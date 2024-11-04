# Generated by Django 5.0.7 on 2024-08-08 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_stop_type_of_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='type_of_stop',
            field=models.CharField(choices=[('sea', 'Sea'), ('cafe', 'Cafe'), ('city', 'City'), ('eating', 'Eating'), ('nature', 'Nature'), ('sightSeeing', 'Sight Seeing'), ('travel', 'Travel'), ('freeTime', 'Free Time'), ('other', 'Other')], default='other', max_length=30),
        ),
    ]
