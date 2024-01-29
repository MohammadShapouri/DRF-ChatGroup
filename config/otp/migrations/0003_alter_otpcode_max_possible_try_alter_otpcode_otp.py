# Generated by Django 4.2.7 on 2023-11-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0002_otpcode_max_possible_try_otpcode_otp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='max_possible_try',
            field=models.PositiveIntegerField(default=5, verbose_name='Maximum possible number of Attempts'),
        ),
        migrations.AlterField(
            model_name='otpcode',
            name='otp',
            field=models.CharField(max_length=6, verbose_name='One Time Password Code'),
        ),
    ]