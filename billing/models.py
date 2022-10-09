import datetime
from django.db import models
from django.utils import timezone
from student.models import std_trx

# Create your models here.
class bll_mst_bill_item(models.Model):
    item_name = models.CharField(max_length=30, db_column="ITEM_NAME")
    debet_credit = models.IntegerField(db_column="DEBET_CREDIT")
    validstatus = models.IntegerField(default=1, blank=True, null=True, db_column="VALID_STATUS")
    date_created = models.DateField(default=datetime.date.today, blank=True, db_column="DATE_CREATED")
    created_by = models.CharField(max_length=30, db_column="CREATED_BY")

    class Meta:
        db_table = 'BLL_MST_BILL_ITEM'

class bll_trx_billing(models.Model):
    invoice_date = models.DateField(default=datetime.date.today, db_column="INVOICE_DATE")
    total_amount = models.DecimalField(db_column="TOTAL_AMOUNT", decimal_places=2, max_digits=12) 
    remarks = models.CharField(max_length=30, db_column="REMARKS")
    date_created = models.DateField(default=timezone.now, blank=True, db_column="DATE_CREATED")
    created_by = models.CharField(max_length=30, db_column="CREATED_BY")
    date_modified = models.DateField(blank=True, null=True, db_column="DATE_MODIFIED")
    modified_by = models.CharField(max_length=30, blank=True, null=True, db_column="MODIFIED_BY")
    std_trx_id = models.ForeignKey(std_trx, on_delete=models.RESTRICT, db_column="STD_TRX_ID")
    tobe_paid = models.DecimalField(db_column="TOBE_PAID", decimal_places=2, max_digits=12) 
    month = models.IntegerField(db_column="MONTH")
    year = models.IntegerField(db_column="YEAR")
    periode = models.IntegerField(db_column="PERIODE")

    class Meta:
        db_table = 'BLL_TRX_BILLING'

class bll_trx_bill_item(models.Model):
    
    description = models.CharField(max_length=30, db_column="DESCRIPTION")
    value = models.IntegerField(db_column="VALUE")
    date_created = models.DateField(default=datetime.date.today, blank=True, db_column="DATE_CREATED")
    created_by = models.CharField(max_length=30, db_column="CREATED_BY")
    date_modified = models.DateField(blank=True, null=True, db_column="DATE_MODIFIED")
    modified_by = models.CharField(max_length=30, blank=True, null=True, db_column="MODIFIED_BY")
    
    btb_id = models.ForeignKey(bll_trx_billing, on_delete=models.RESTRICT, db_column="BLL_TRX_BILLING_ID")
    bll_mst_id = models.ForeignKey(bll_mst_bill_item, on_delete=models.RESTRICT, db_column="BLL_MST_BILL_ITEM_ID")
    std_trx_id = models.ForeignKey(std_trx, on_delete=models.RESTRICT, db_column="STD_TRX_ID")
    class Meta:
        db_table = 'BLL_TRX_BILL_ITEM'