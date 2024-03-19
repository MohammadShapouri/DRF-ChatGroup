# Generated by Django 4.2.7 on 2024-03-19 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatGroup', '0002_chatgroup_media_uploading_access_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='add_users_by_members',
            field=models.BooleanField(default=True, verbose_name='Can other users add new members?'),
        ),
    ]