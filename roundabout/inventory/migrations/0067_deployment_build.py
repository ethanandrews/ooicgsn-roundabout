# Generated by Django 2.2.1 on 2019-06-26 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0004_auto_20190626_1551'),
        ('inventory', '0066_inventory_build'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='build',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deployments', to='builds.Build'),
        ),
    ]