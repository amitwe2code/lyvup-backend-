# Generated by Django 5.1.3 on 2024-12-03 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0013_usermodel_account_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='user_permissions',
        ),
    ]
