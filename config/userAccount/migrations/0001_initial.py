# Generated by Django 4.2.7 on 2023-11-13 08:32

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid phone number. Please enter a phone number with correct format.', regex='09(0[0-3]|1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}')], verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('is_account_verified', models.BooleanField(default=False, verbose_name='Is Account Verified?')),
                ('new_phone_number', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='Invalid phone number. Please enter a phone number with correct format.', regex='09(0[0-3]|1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}')], verbose_name='Phone Number')),
                ('is_new_phone_verified', models.BooleanField(default=True, verbose_name='Is New Phone Number Verified?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User Account',
                'verbose_name_plural': 'User Accounts',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
