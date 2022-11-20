# Generated by Django 4.1 on 2022-10-09 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_std_trx_course_amount_hour_and_more'),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bll_trx_bill_item',
            name='std_trx_course_id',
            field=models.ForeignKey(db_column='STD_TRX_COURSE_ID', default=1, on_delete=django.db.models.deletion.RESTRICT, to='student.std_trx_course'),
            preserve_default=False,
        ),
    ]