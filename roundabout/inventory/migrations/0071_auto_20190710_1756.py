# Generated by Django 2.2.1 on 2019-07-10 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0070_deployment_deployed_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deployment',
            options={'ordering': ['build', '-created_at']},
        ),
    ]