# Generated by Django 4.2.17 on 2024-12-31 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_intervention_indicate_when_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervention',
            name='todo',
        ),
    ]