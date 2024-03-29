# Generated by Django 4.2.7 on 2023-11-30 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userAccount.models


class Migration(migrations.Migration):

    dependencies = [
        ('userAccount', '0003_alter_useraccount_new_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccountProfilePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=userAccount.models.set_filename, verbose_name='Profile Picture')),
                ('is_default_pic', models.BooleanField(default=True, verbose_name='Is It Default Profile Picture?')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name="This Profile Picture's Creation Date")),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rofilePicture', to=settings.AUTH_USER_MODEL, verbose_name='User Account Profile Picture')),
            ],
            options={
                'verbose_name': 'User Account Profile Picture',
                'verbose_name_plural': 'User Account Profile Pictures',
            },
        ),
    ]
