# Generated by Django 5.0.7 on 2024-08-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_alter_lodging_note_alter_stop_note_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='ltd',
            field=models.FloatField(blank=True, null=True),
        ),
    ]