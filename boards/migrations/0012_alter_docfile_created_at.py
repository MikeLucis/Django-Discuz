# Generated by Django 3.2.9 on 2022-03-27 14:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('boards', '0011_auto_20220327_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docfile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
