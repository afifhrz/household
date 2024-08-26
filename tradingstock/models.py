from django.db import models
from django.utils import timezone

# Create your models here.
        
class trd_mst_stock(models.Model):
    date_modified = models.DateTimeField(default=timezone.now, db_column="MODIFIED_DATE")
    stock_code = models.CharField(max_length=30, db_column="CODE", unique=True) 
    valid_status = models.BooleanField(db_column="VALID_STATUS")
    owned = models.BooleanField(db_column="OWNED", default=False)
    buy_price = models.IntegerField(db_column="BUY_PRICE", default=0, null=True, blank=True)

    class Meta:
        db_table = 'TRD_MST_STOCK'
        
        
class trd_filtered_stock(models.Model):
    mst_id = models.ForeignKey(trd_mst_stock, on_delete=models.RESTRICT, db_column="TRD_MST_STOCK")
    date_modified = models.DateTimeField(default=timezone.now, db_column="MODIFIED_DATE")
    last_price = models.IntegerField(db_column="LAST_PRICE", default="", null=True, blank=True)
    last_open = models.IntegerField(db_column="LAST_OPEN", default=0)
    ma_d_3 = models.IntegerField(db_column="MA_D_3")
    ma_d_5 = models.IntegerField(db_column="MA_D_5")
    ma_d_7 = models.IntegerField(db_column="MA_D_7")
    ma_d_10 = models.IntegerField(db_column="MA_D_10")
    ma_d_14 = models.IntegerField(db_column="MA_D_14")
    ma_d_18 = models.IntegerField(db_column="MA_D_18")
    ma_d_50 = models.IntegerField(db_column="MA_D_50")
    ma_d_100 = models.IntegerField(db_column="MA_D_100")
    ma_d_200 = models.IntegerField(db_column="MA_D_200")
    status = models.TextField(max_length=30, db_column="STATUS", null=True, blank=True)

    class Meta:
        db_table = 'TRD_FILTERED_STOCK'

class trd_trx_stock(models.Model):
    date_created = models.DateTimeField(default=timezone.now, db_column="CREATED_DATE")
    mst_id = models.ForeignKey(trd_mst_stock, on_delete=models.RESTRICT, db_column="TRD_MST_STOCK")
    lot = models.IntegerField(db_column="LOT")
    price = models.IntegerField(db_column="PRICE", default="", null=True, blank=True)
    amount = models.FloatField(db_column="AMOUNT")
    is_last_transaction = models.BooleanField(db_column="IS_LAST_TRANSACTION", default=False)

    class Meta:
        db_table = 'TRD_TRX_STOCK'