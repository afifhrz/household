# Generated by Django 4.1 on 2023-12-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automotive', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto_mst_service_item',
            name='validstatus',
            field=models.IntegerField(blank=True, db_column='VALID_STATUS', default=1, null=True),
        ),
    ]
