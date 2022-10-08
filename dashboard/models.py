import datetime
from django.db import models

# Create your models here.
class admin_mst_module(models.Model):
    modulename = models.CharField(max_length=30, db_column="MODULENAME")
    pagename = models.CharField(max_length=30, db_column="PAGENAME")
    created_by = models.CharField(max_length=30, db_column="CREATED_BY")
    date_created = models.DateField(default=datetime.date.today, blank=True, db_column="DATE_CREATED")
    modified_by = models.CharField(max_length=30, blank=True, null=True, db_column="MODIFIED_BY")
    date_modified = models.DateField(blank=True, null=True, db_column="DATE_MODIFIED")
    adm_mst_id = models.IntegerField(blank=True, null=True, db_column="ADM_MST_MODULE_ID")
    validstatus = models.IntegerField(blank=True, null=True, db_column="VALIDSTATUS")
    ordernumber = models.IntegerField(db_column="ORDERNUMBER")
    levelnumber = models.IntegerField(blank=True, null=True, db_column="LEVELNUMBER")
    moduleurl = models.CharField(max_length=30, blank=True, null=True, db_column="MODULEURL")
    moduleicon = models.CharField(max_length=30, blank=True, null=True, db_column="MODULEICON")
    moduleclass = models.CharField(max_length=30, blank=True, null=True, db_column="MODULECLASS")
    application = models.CharField(max_length=30, db_column="APPLICATION")

    class Meta:
        db_table = 'ADM_MST_MODULE'