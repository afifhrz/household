# Generated by Django 4.1 on 2023-09-25 12:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_alter_acc_ar_debt_account_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_ar_debt',
            name='account_date',
            field=models.DateTimeField(db_column='ACCOUNT_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 443805)),
        ),
        migrations.AlterField(
            model_name='acc_income_expense',
            name='account_date',
            field=models.DateTimeField(db_column='ACCOUNT_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 443805)),
        ),
        migrations.AlterField(
            model_name='acc_investment_deposit',
            name='date_created',
            field=models.DateTimeField(db_column='CREATED_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 459436)),
        ),
        migrations.AlterField(
            model_name='acc_investment_fund',
            name='date_modified',
            field=models.DateTimeField(db_column='MODIFIED_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 459436)),
        ),
        migrations.AlterField(
            model_name='acc_investment_fund',
            name='fund_code',
            field=models.CharField(db_column='FUND_NAME', max_length=100),
        ),
        migrations.AlterField(
            model_name='acc_investment_stock',
            name='date_modified',
            field=models.DateTimeField(db_column='MODIFIED_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 443805)),
        ),
        migrations.AlterField(
            model_name='acc_investment_stock',
            name='last_price_date',
            field=models.DateTimeField(db_column='LAST__PRICE_UPDATE_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 443805)),
        ),
        migrations.AlterField(
            model_name='acc_saving_goal_tracker',
            name='date_created',
            field=models.DateTimeField(db_column='CREATED_DATE', default=datetime.datetime(2023, 9, 25, 19, 5, 19, 459436)),
        ),
    ]
