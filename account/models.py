from django.db import models
from datetime import datetime
from billing.models import bll_mst_bill_item

# Create your models here.
class acc_income_expense(models.Model):
    account_type = models.CharField(default='Bank BRI', max_length=30, db_column="ACCOUNT_TYPE")
    account_date = models.DateTimeField(default=datetime.now(), db_column="ACCOUNT_DATE")
    description = models.CharField(max_length=30, db_column="DESCRIPTION")
    remarks = models.CharField(max_length=100, db_column="REMARKS", default='', null=True, blank=True)
    amount_in = models.DecimalField(db_column="AMOUNT_IN", blank=True, null=True, decimal_places=2, max_digits=20) 
    amount_out = models.DecimalField(db_column="AMOUNT_OUT", blank=True, null=True, decimal_places=2, max_digits=20)
    overall_balance = models.DecimalField(db_column="OVERALL_BALANCE", decimal_places=2, max_digits=20) 
    bll_mst_item_id = models.ForeignKey(bll_mst_bill_item, on_delete=models.RESTRICT, db_column="BLL_MST_BILL_ITEM_ID", default=1)

    class Meta:
        db_table = 'ACC_INC_EXP'

class acc_ar_debt(models.Model):
    account_date = models.DateTimeField(default=datetime.now(), db_column="ACCOUNT_DATE")
    description = models.CharField(max_length=30, db_column="DESCRIPTION") 
    amount = models.DecimalField(db_column="AMOUNT", blank=True, null=True, decimal_places=2, max_digits=20)
    account_status = models.CharField(max_length=30, db_column="ACCOUNT_STATUS")
    account_type = models.CharField(max_length=30, db_column="ACCOUNT_TYPE")
    bll_mst_item_id = models.ForeignKey(bll_mst_bill_item, on_delete=models.RESTRICT, db_column="BLL_MST_BILL_ITEM_ID", default=1)
    valid_status = models.CharField(max_length=30, db_column="VALID_STATUS")

    class Meta:
        db_table = 'ACC_AR_DEBT'

class acc_investment_stock(models.Model):
    date_modified = models.DateTimeField(default=datetime.now(), db_column="MODIFIED_DATE")
    stock_code = models.CharField(max_length=30, db_column="STOCKS") 
    average = models.DecimalField(db_column="AVERAGE_PRICE", blank=True, null=True, decimal_places=2, max_digits=20)
    der_annual = models.DecimalField(db_column="DER_ANNUAL", blank=True, null=True, decimal_places=2, max_digits=20)
    bv_5 = models.DecimalField(db_column="BV_5", blank=True, null=True, decimal_places=2, max_digits=20)
    bv_annual = models.DecimalField(db_column="BV_ANNUAL", blank=True, null=True, decimal_places=2, max_digits=20)
    dividend = models.DecimalField(db_column="DIVIDEND", blank=True, null=True, decimal_places=2, max_digits=20)
    lot = models.IntegerField(db_column="LOT")
    last_price = models.IntegerField(db_column="LAST_PRICE", default="", null=True, blank=True)
    last_price_date = models.DateTimeField(default=datetime.now(), db_column="LAST__PRICE_UPDATE_DATE")

    class Meta:
        db_table = 'ACC_INVESTMENT_STOCK'
        
class acc_investment_fund(models.Model):
    date_modified = models.DateTimeField(default=datetime.now(), db_column="MODIFIED_DATE")
    fund_code = models.CharField(max_length=30, db_column="FUND_NAME") 
    average_nav = models.DecimalField(db_column="AVERAGE_NAV", blank=True, null=True, decimal_places=2, max_digits=20)
    current_nav = models.DecimalField(db_column="CURRENT_NAV", blank=True, null=True, decimal_places=2, max_digits=20)
    unit = models.DecimalField(db_column="UNIT", blank=True, null=True, decimal_places=2, max_digits=20)

    class Meta:
        db_table = 'ACC_INVESTMENT_FUND'
        
class acc_investment_deposit(models.Model):
    date_created = models.DateTimeField(default=datetime.now(), db_column="CREATED_DATE")
    description = models.CharField(max_length=30, db_column="DESCRIPTION") 
    amount = models.DecimalField(db_column="AMOUNT", blank=True, null=True, decimal_places=2, max_digits=20)

    class Meta:
        db_table = 'ACC_INVESTMENT_DEPOSIT'