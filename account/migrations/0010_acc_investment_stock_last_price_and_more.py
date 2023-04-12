# Generated by Django 4.1 on 2023-04-09 16:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_acc_ar_debt_account_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='acc_investment_stock',
            name='last_price',
            field=models.IntegerField(blank=True, db_column='LAST_PRICE', default=0, null=True),
        ),
        migrations.AddField(
            model_name='acc_investment_stock',
            name='last_price_date',
            field=models.DateTimeField(db_column='LAST__PRICE_UPDATE_DATE', default=datetime.datetime(2023, 4, 9, 23, 34, 16, 840125)),
        ),
        migrations.AlterField(
            model_name='acc_ar_debt',
            name='account_date',
            field=models.DateTimeField(db_column='ACCOUNT_DATE', default=datetime.datetime(2023, 4, 9, 23, 34, 16, 840125)),
        ),
        migrations.AlterField(
            model_name='acc_income_expense',
            name='account_date',
            field=models.DateTimeField(db_column='ACCOUNT_DATE', default=datetime.datetime(2023, 4, 9, 23, 34, 16, 840125)),
        ),
        migrations.AlterField(
            model_name='acc_investment_deposit',
            name='date_created',
            field=models.DateTimeField(db_column='CREATED_DATE', default=datetime.datetime(2023, 4, 9, 23, 34, 16, 841125)),
        ),
        migrations.AlterField(
            model_name='acc_investment_fund',
            name='date_modified',
            field=models.DateTimeField(db_column='MODIFIED_DATE', default=datetime.datetime(2023, 4, 9, 23, 34, 16, 840125)),
        ),
        migrations.AlterField(
            model_name='acc_investment_stock',
            name='date_modified',
            field=models.DateTimeField(db_column='MODIFIED_DATE', default=datetime.datetime(2023, 4, 9, 23, 34, 16, 840125)),
        ),
    ]
