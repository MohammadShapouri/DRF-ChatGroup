# Generated by Django 4.2.7 on 2023-12-01 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userAccount', '0004_useraccountprofilepicture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccountprofilepicture',
            old_name='image',
            new_name='photo',
        ),
    ]
