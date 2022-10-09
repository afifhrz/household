import datetime
from django.db import models

# Create your models here.
class prd_mst(models.Model):
    course_name = models.CharField(max_length=30, db_column="COURSE_NAME")
    description = models.CharField(max_length=30, db_column="DESCRIPTION")
    validuntil = models.DateField(blank=True, null=True, db_column="VALID_UNTIL")
    remarks = models.CharField(max_length=30, blank=True, null=True, db_column="REMARKS")
    date_created = models.DateField(default=datetime.date.today, blank=True, db_column="DATE_CREATED")
    created_by = models.CharField(max_length=30, db_column="CREATED_BY")
    date_modified = models.DateField(blank=True, null=True, db_column="DATE_MODIFIED")
    modified_by = models.CharField(max_length=30, blank=True, null=True, db_column="MODIFIED_BY")

    class Meta:
        db_table = 'PRD_MST'