# Generated by Django 5.0.7 on 2024-08-09 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_alter_stop_type_of_stop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lodging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start_date', models.DateField(verbose_name='start_date')),
                ('end_date', models.DateField(verbose_name='end_date')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.location')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.trip')),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('dateAndTime', models.DateTimeField(null=True)),
                ('type_of_transport', models.CharField(choices=[('plane', 'Plane'), ('train', 'Train'), ('bus', 'Bus'), ('ferry', 'Ferry')], default='freeTime', max_length=30)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.location')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.trip')),
            ],
        ),
    ]
