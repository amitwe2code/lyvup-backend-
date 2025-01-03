# Generated by Django 4.2.17 on 2024-12-31 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activityapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityactiontype',
            name='activity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='activityactiontype',
            name='activity_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='activityactiontype',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='activityactiontype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='activityactiontype',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='activityactiontype',
            name='key_activity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='activityactiontype',
            name='unit',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='activityactiontype',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]