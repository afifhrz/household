import datetime
from django.db import models
from django.utils import timezone
from product.models import prd_mst

# Create your models here.
class std_mst(models.Model):
    name = models.CharField(max_length=30, db_column="NAME")
    phone = models.CharField(max_length=30, db_column="BOOKED_PHONE")
    email = models.CharField(max_length=30, db_column="EMAIL")
    address = models.CharField(max_length=30, blank=True, null=True, db_column="ADDRESS")
    validuntil = models.DateField(blank=True, null=True, db_column="VALID_UNTIL")
    date_created = models.DateField(default=datetime.date.today, blank=True, db_column="DATE_CREATED")
    created_by = models.CharField(max_length=30, db_column="CREATED_BY")
    date_modified = models.DateField(blank=True, null=True, db_column="DATE_MODIFIED")
    modified_by = models.CharField(max_length=30, blank=True, null=True, db_column="MODIFIED_BY")
    reason = models.CharField(max_length=30, blank=True, null=True, db_column="REASON_TERMINATE")

    class Meta:
        db_table = 'STD_MST'

class std_trx(models.Model):
    std_mst_id = models.ForeignKey(std_mst, on_delete=models.RESTRICT, db_column="STD_MST_ID")
    prd_mst_id = models.ForeignKey(prd_mst, on_delete=models.RESTRICT, db_column="PRD_MST_ID")
    phone = models.CharField(max_length=30, db_column="STUDENT_PHONE")
    email = models.CharField(max_length=30, db_column="STUDENT_EMAIL")
    amount = models.IntegerField(db_column="AMOUNT")
    validuntil = models.DateField(blank=True, null=True, db_column="VALID_UNTIL")
    date_created = models.DateField(default=datetime.date.today, blank=True, db_column="DATE_CREATED")
    created_by = models.CharField(max_length=30, db_column="CREATED_BY")
    date_modified = models.DateField(blank=True, null=True, db_column="DATE_MODIFIED")
    modified_by = models.CharField(max_length=30, blank=True, null=True, db_column="MODIFIED_BY")
    remarks = models.CharField(max_length=30, blank=True, null=True, db_column="REMARKS")

    class Meta:
        db_table = 'STD_TRX'

class std_trx_course(models.Model):
    std_trx_id = models.ForeignKey(std_trx, on_delete=models.RESTRICT, db_column="STD_TRX_ID")
    date_time = models.DateTimeField(default=timezone.now, blank=True, db_column="DATETIME")
    amount_hour = models.DecimalField(db_column="AMOUNT_HOUR", decimal_places=2, max_digits=4)
    validuntil = models.DateField(blank=True, null=True, db_column="VALID_UNTIL")
    date_created = models.DateField(default=timezone.now, blank=True, db_column="DATE_CREATED")
    created_by = models.CharField(max_length=30, db_column="CREATED_BY")
    date_modified = models.DateField(blank=True, null=True, db_column="DATE_MODIFIED")
    modified_by = models.CharField(max_length=30, blank=True, null=True, db_column="MODIFIED_BY")

    class Meta:
        db_table = 'STD_TRX_COURSE'