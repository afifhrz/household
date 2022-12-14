# Generated by Django 4.1 on 2022-10-16 04:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_bll_trx_billing_invoice_status'),
        ('account', '0002_acc_income_expense_account_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='acc_income_expense',
            name='bll_mst_item_id',
            field=models.ForeignKey(db_column='BLL_MST_BILL_ITEM_ID', default=1, on_delete=django.db.models.deletion.RESTRICT, to='billing.bll_mst_bill_item'),
        ),
        migrations.AlterField(
            model_name='acc_income_expense',
            name='account_date',
            field=models.DateTimeField(db_column='ACCOUNT_DATE', default=datetime.datetime(2022, 10, 16, 11, 7, 20, 815456)),
        ),
    ]
