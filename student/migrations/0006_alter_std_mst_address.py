# Generated by Django 4.1 on 2023-09-25 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_std_mst_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='std_mst',
            name='address',
            field=models.CharField(blank=True, db_column='ADDRESS', max_length=100, null=True),
        ),
    ]
