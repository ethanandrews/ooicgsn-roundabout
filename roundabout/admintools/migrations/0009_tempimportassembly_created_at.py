# Generated by Django 2.2.9 on 2020-01-14 16:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admintools', '0008_auto_20200114_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempimportassembly',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]