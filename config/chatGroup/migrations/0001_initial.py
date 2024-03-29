# Generated by Django 4.2.7 on 2024-01-29 07:41

import chatGroup.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=25, verbose_name='Chat Group Name')),
                ('bio', models.CharField(blank=True, max_length=75, null=True, verbose_name='Chat Group Bio')),
                ('group_special_username', models.SlugField(blank=True, null=True, validators=[django.core.validators.RegexValidator(flags=re.RegexFlag['ASCII'], message='Enter a valid username. This value may contain only English letters, numbers, and @/./+/-/_ characters.', regex='^[\\w.]+\\Z')], verbose_name='Chat Group Special Username Link')),
                ('group_random_username', models.SlugField(blank=True, null=True, unique=True, verbose_name='Chat Group Random Username Link')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is Chat Group Public?')),
                ('is_forward_allowed', models.BooleanField(default=True, verbose_name='Is Forward Allowed?')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
            ],
            options={
                'verbose_name': 'Chat Group',
                'verbose_name_plural': 'Chat Groups',
            },
        ),
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=chatGroup.models.update_filename, verbose_name='File')),
            ],
            options={
                'verbose_name': 'Message File',
                'verbose_name_plural': 'Message Files',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500, verbose_name='Message')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('chat_group', models.ManyToManyField(to='chatGroup.chatgroup', verbose_name='Related Chat Group')),
                ('file', models.ManyToManyField(to='chatGroup.messagefile', verbose_name='Message File')),
                ('replied_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='chatGroup.message', verbose_name='Replied to')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Writer')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='ChatGroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.CharField(choices=[('normal_user', 'Normal User'), ('admin', 'Admin'), ('owner', 'Owner')], max_length=11, verbose_name='User Access Level')),
                ('member_nickname', models.CharField(blank=True, max_length=20, null=True, verbose_name='Nickname')),
                ('joined_at', models.DateTimeField(auto_now_add=True, verbose_name='Joining Date')),
                ('chat_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatGroup.chatgroup', verbose_name='Related Chat Group')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Joined User')),
            ],
            options={
                'verbose_name': 'Chat Group Member',
                'verbose_name_plural': 'Chat Group Members',
            },
        ),
    ]
