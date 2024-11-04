# Generated by Django 5.0.7 on 2024-08-22 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_rename_start_date_stop_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stop',
            name='location',
        ),
        migrations.RemoveField(
            model_name='lodging',
            name='location',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='location',
        ),
        migrations.AddField(
            model_name='lodging',
            name='lng',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lodging',
            name='ltd',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stop',
            name='lng',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stop',
            name='ltd',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transport',
            name='lng',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transport',
            name='ltd',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]