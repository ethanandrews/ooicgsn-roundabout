# Generated by Django 2.2.1 on 2019-07-08 17:12

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0011_location_root_type'),
        ('inventory', '0069_inventory_assembly_part'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='deployed_location',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deployed_deployments', to='locations.Location'),
        ),
    ]