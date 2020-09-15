# Generated by Django 3.1 on 2020-09-13 16:05

from django.db import migrations
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('create_join_class', '0013_readinginfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingmaterial',
            name='readingFile',
            field=private_storage.fields.PrivateFileField(storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='uploads/ReadingMaterial/'),
        ),
    ]