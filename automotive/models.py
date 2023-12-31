from django.db import models
from datetime import datetime

# Create your models here.
class auto_mst_vehicle(models.Model):
    name = models.CharField(max_length=30, db_column="VEHICLE_NAME")
    year = models.IntegerField(db_column="YEAR")
    current_kilometer = models.IntegerField(db_column="CURRENT_KILOMETER")
    validstatus = models.IntegerField(default=1, blank=True, null=True, db_column="VALID_STATUS")
    date_created = models.DateField(default=datetime.now, blank=True, db_column="DATE_CREATED")

    class Meta:
        db_table = 'AUTO_MST_VEHICLE'

class auto_mst_service_item(models.Model):
    service_name = models.CharField(max_length=30, db_column="SERVICE_NAME")
    repeating_kilometer = models.IntegerField(db_column="REPEATING_KILOMETER", default=0)
    repeating_months = models.IntegerField(db_column="REPEATING_MONTHS", default=0)
    # Inspect, Adjustment, Replace
    service_type = models.CharField(max_length=30, db_column="SERVICE_TYPE")
    vehicle_id = models.ForeignKey(auto_mst_vehicle, on_delete=models.RESTRICT, db_column="VEHICLE_ID")
    
    date_created = models.DateTimeField(default=datetime.now, blank=True, db_column="DATE_CREATED")
    validstatus = models.IntegerField(default=1, blank=True, null=True, db_column="VALID_STATUS")

    class Meta:
        db_table = 'AUTO_MST_SERVICE_ITEM'

class auto_service_history(models.Model):
    auto_mst_service_item_id = models.ForeignKey(auto_mst_service_item, on_delete=models.RESTRICT, db_column="AUTO_MST_SERVICE_ITEM_ID")
    price = models.IntegerField(db_column="PRICE")
    last_service_kilometer = models.IntegerField(db_column="LAST_SERVICE_KILOMETER")
    last_service_date = models.DateField(default=datetime.now, db_column="LAST_SERVICE_DATE")
    next_service_kilometer = models.IntegerField(db_column="NEXT_SERVICE_KILOMETER")
    next_service_date = models.DateField(default=datetime.now, blank=True, db_column="NEXT_SERVICE_DATE")
    note = models.CharField(max_length=256, db_column="NOTE")
    date_created = models.DateField(default=datetime.now, blank=True, db_column="DATE_CREATED")
    validstatus = models.IntegerField(default=1, blank=True, null=True, db_column="VALID_STATUS")
    
    class Meta:
        db_table = 'AUTO_SERVICE_HISTORY'