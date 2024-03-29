# Generated by Django 4.1 on 2023-07-25 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradingstock', '0004_alter_trd_filtered_stock_date_modified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trd_filtered_stock',
            name='date_modified',
            field=models.DateTimeField(db_column='MODIFIED_DATE', default=datetime.datetime(2023, 7, 25, 22, 41, 5, 942289)),
        ),
        migrations.AlterField(
            model_name='trd_filtered_stock',
            name='last_open',
            field=models.IntegerField(db_column='LAST_OPEN', default=0, null=True),
        ),
        migrations.AlterField(
            model_name='trd_mst_stock',
            name='date_modified',
            field=models.DateTimeField(db_column='MODIFIED_DATE', default=datetime.datetime(2023, 7, 25, 22, 41, 5, 941921)),
        ),
        migrations.AlterField(
            model_name='trd_trx_stock',
            name='date_created',
            field=models.DateTimeField(db_column='CREATED_DATE', default=datetime.datetime(2023, 7, 25, 22, 41, 5, 942289)),
        ),
    ]
