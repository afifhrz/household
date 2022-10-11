from django.db import models
from datetime import datetime

# Create your models here.
class acc_income_expense(models.Model):
    account_type = models.CharField(default='Bank BRI', max_length=30, db_column="ACCOUNT_TYPE")
    account_date = models.DateTimeField(default=datetime.now(), db_column="ACCOUNT_DATE")
    description = models.CharField(max_length=30, db_column="DESCRIPTION")
    category = models.CharField(max_length=30, db_column="CATEGORY")
    amount_in = models.DecimalField(db_column="AMOUNT_IN", blank=True, null=True, decimal_places=2, max_digits=20) 
    amount_out = models.DecimalField(db_column="AMOUNT_OUT", blank=True, null=True, decimal_places=2, max_digits=20)
    overall_balance = models.DecimalField(db_column="OVERALL_BALANCE", decimal_places=2, max_digits=20) 

    class Meta:
        db_table = 'ACC_INC_EXP'