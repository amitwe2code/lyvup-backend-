# Generated by Django 4.2.17 on 2025-01-09 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_alter_activity_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(blank=True, choices=[('survey', 'survey'), ('challenge', 'challenge'), ('interview', 'interview'), ('video', 'video'), ('podcast', 'podcast'), ('workshop', 'workshop'), ('assignment', 'assignment'), ('excercise', 'excercise'), ('other', 'other')], max_length=50, null=True),
        ),
    ]