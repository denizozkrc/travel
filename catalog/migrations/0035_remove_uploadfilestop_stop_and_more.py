# Generated by Django 5.0.7 on 2024-09-02 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0034_alter_uploadfilelodging_type_of_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfilestop',
            name='stop',
        ),
        migrations.RemoveField(
            model_name='uploadfiletransport',
            name='transport',
        ),
        migrations.DeleteModel(
            name='UploadFileLodging',
        ),
        migrations.DeleteModel(
            name='UploadFileStop',
        ),
        migrations.DeleteModel(
            name='UploadFileTransport',
        ),
    ]