# Generated by Django 4.1 on 2022-10-08 11:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_prd_mst_remarks'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='std_trx',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(db_column='STUDENT_PHONE', max_length=30)),
                ('email', models.CharField(db_column='STUDENT_EMAIL', max_length=30)),
                ('amount', models.IntegerField(db_column='AMOUNT')),
                ('validuntil', models.DateField(blank=True, db_column='VALID_UNTIL', null=True)),
                ('date_created', models.DateField(blank=True, db_column='DATE_CREATED', default=datetime.date.today)),
                ('created_by', models.CharField(db_column='CREATED_BY', max_length=30)),
                ('date_modified', models.DateField(blank=True, db_column='DATE_MODIFIED', null=True)),
                ('modified_by', models.CharField(blank=True, db_column='MODIFIED_BY', max_length=30, null=True)),
                ('remarks', models.CharField(blank=True, db_column='REMARKS', max_length=30, null=True)),
                ('prd_mst_id', models.ForeignKey(db_column='PRD_MST_ID', on_delete=django.db.models.deletion.RESTRICT, to='product.prd_mst')),
                ('std_mst_id', models.ForeignKey(db_column='STD_MST_ID', on_delete=django.db.models.deletion.RESTRICT, to='student.std_mst')),
            ],
            options={
                'db_table': 'STD_TRX',
            },
        ),
    ]
