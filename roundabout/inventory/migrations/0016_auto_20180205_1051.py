# Generated by Django 2.0 on 2018-02-05 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_auto_20180131_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='serial_number',
            field=models.CharField(max_length=255),
        ),
    ]
