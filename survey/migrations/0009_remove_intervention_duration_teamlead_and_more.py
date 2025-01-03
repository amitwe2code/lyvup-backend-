# Generated by Django 4.2.17 on 2024-12-31 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_remove_intervention_costs_remove_intervention_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervention',
            name='duration_teamlead',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='indicate_when_completed',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='travel_time',
        ),
        migrations.AlterField(
            model_name='intervention',
            name='activity_type',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='completion_check',
            field=models.CharField(blank=True, null=True),
        ),
    ]