# Generated by Django 2.0.9 on 2018-12-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0049_auto_20181024_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_type',
            field=models.CharField(choices=[('invadd', 'Add Inventory'), ('invchange', 'Inventory Change'), ('locationchange', 'Location Change'), ('subchange', 'Subassembly Change'), ('addtodeployment', 'Add to Deployment'), ('removefromdeployment', 'Remove from Deployment'), ('deploymentburnin', 'Deployment Burnin'), ('deploymenttosea', 'Deployment to Sea'), ('deploymentrecover', 'Deployment Recovered'), ('assigndest', 'Assign Destination'), ('removedest', 'Remove Destination'), ('test', 'Test'), ('note', 'Note'), ('historynote', 'Historical Note'), ('ticket', 'Work Ticket'), ('flag', 'Flag'), ('movetotrash', 'Move to Trash')], max_length=20),
        ),
    ]
