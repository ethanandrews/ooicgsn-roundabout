# Generated by Django 2.0 on 2018-01-05 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_deployment'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='deployment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory', to='inventory.Deployment'),
        ),
    ]
