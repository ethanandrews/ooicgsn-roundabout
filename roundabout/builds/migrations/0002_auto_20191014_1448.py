"""
# Copyright (C) 2019-2020 Woods Hole Oceanographic Institution
#
# This file is part of the Roundabout Database project ("RDB" or 
# "ooicgsn-roundabout").
#
# ooicgsn-roundabout is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# ooicgsn-roundabout is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ooicgsn-roundabout in the COPYING.md file at the project root.
# If not, see <http://www.gnu.org/licenses/>.
"""

# Generated by Django 2.2.4 on 2019-10-14 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
        ('builds', '0001_initial'),
        ('assemblies', '0001_initial'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorysnapshot',
            name='inventory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_snapshots', to='inventory.Inventory'),
        ),
        migrations.AddField(
            model_name='inventorysnapshot',
            name='location',
            field=mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_snapshots', to='locations.Location'),
        ),
        migrations.AddField(
            model_name='inventorysnapshot',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='builds.InventorySnapshot'),
        ),
        migrations.AddField(
            model_name='buildsnapshot',
            name='build',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='build_snapshots', to='builds.Build'),
        ),
        migrations.AddField(
            model_name='buildsnapshot',
            name='deployment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='build_snapshots', to='inventory.Deployment'),
        ),
        migrations.AddField(
            model_name='buildsnapshot',
            name='location',
            field=mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='build_snapshots', to='locations.Location'),
        ),
        migrations.AddField(
            model_name='buildaction',
            name='build',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='builds.Build'),
        ),
        migrations.AddField(
            model_name='buildaction',
            name='location',
            field=mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actions', to='locations.Location'),
        ),
        migrations.AddField(
            model_name='buildaction',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='build',
            name='assembly',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='assemblies.Assembly'),
        ),
        migrations.AddField(
            model_name='build',
            name='location',
            field=mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='builds', to='locations.Location'),
        ),
    ]
