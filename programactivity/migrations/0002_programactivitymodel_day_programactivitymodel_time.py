# Generated by Django 5.1.3 on 2025-01-13 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programactivity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='programactivitymodel',
            name='day',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='programactivitymodel',
            name='time',
            field=models.FloatField(blank=True, null=True),
        ),
    ]