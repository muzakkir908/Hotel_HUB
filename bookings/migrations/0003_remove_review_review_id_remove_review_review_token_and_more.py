# Generated by Django 4.2.20 on 2025-03-28 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_alter_review_unique_together_review_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='review_id',
        ),
        migrations.RemoveField(
            model_name='review',
            name='review_token',
        ),
        migrations.RemoveField(
            model_name='review',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='review',
            name='verified',
        ),
    ]
