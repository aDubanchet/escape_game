# Generated by Django 3.1.5 on 2021-01-21 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210120_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_name_updated_by',
            field=models.CharField(default='admin', max_length=16),
        ),
    ]