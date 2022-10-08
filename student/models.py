import datetime
from django.db import models

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