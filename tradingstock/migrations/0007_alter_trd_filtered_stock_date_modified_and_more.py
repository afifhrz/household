# Generated by Django 4.1 on 2023-09-25 12:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradingstock', '0006_alter_trd_filtered_stock_date_modified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trd_filtered_stock',
            name='date_modified',
            field=models.DateTimeField(db_column='MODIFIED_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 459436)),
        ),
        migrations.AlterField(
            model_name='trd_mst_stock',
            name='date_modified',
            field=models.DateTimeField(db_column='MODIFIED_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 459436)),
        ),
        migrations.AlterField(
            model_name='trd_trx_stock',
            name='date_created',
            field=models.DateTimeField(db_column='CREATED_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 459436)),
        ),
    ]