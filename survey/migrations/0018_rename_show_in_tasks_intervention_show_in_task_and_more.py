# Generated by Django 5.1.3 on 2025-01-02 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0017_rename_duration_coach_intervention_coach_duration_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intervention',
            old_name='show_in_tasks',
            new_name='show_in_task',
        ),
        migrations.AlterField(
            model_name='intervention',
            name='indicate_when_completed',
            field=models.CharField(blank=True, default='no', null=True),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='upload_possible',
            field=models.CharField(blank=True, default='no', null=True),
        ),
    ]