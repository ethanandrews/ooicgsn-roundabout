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

import os
import datetime
from datetime import timedelta

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from model_utils import FieldTracker

from roundabout.locations.models import Location
from roundabout.assemblies.models import Assembly
from roundabout.users.models import User

# Build model

class Build(models.Model):
    FLAG_TYPES = (
            (True, "Flagged"),
            (False, "Unflagged"),
    )
    build_number = models.CharField(max_length=255, unique=False, db_index=True)
    location = TreeForeignKey(Location, related_name='builds',
                              on_delete=models.SET_NULL, null=True, blank=False)
    assembly = models.ForeignKey(Assembly, related_name='builds',
                             on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    build_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    detail = models.TextField(blank=True)
    is_deployed = models.BooleanField(default=False)
    time_at_sea = models.DurationField(default=timedelta(minutes=0), null=True, blank=True)
    flag = models.BooleanField(choices=FLAG_TYPES, blank=False, default=False)

    tracker = FieldTracker(fields=['location',])

    class Meta:
        ordering = ['assembly', 'build_number']

    def __str__(self):
        return '%s - %s' % (self.build_number, self.assembly.name)

    @property
    def name(self):
        return self.assembly.name

    # method to set the object_type variable to send to Javascript AJAX functions
    def get_object_type(self):
        return 'builds'

    def current_deployment(self):
        # set default to None
        current_deployment = None

        if self.is_deployed:
            # get the latest deployment if available
            current_deployment = self.deployments.first()
        return current_deployment
    """
    def current_deployment_status(self):
        # set default deployment_status to None
        deployment_status = None

        # get the latest deployment if available
        latest_deployment = self.deployments.first()
        if latest_deployment:
            deployment_action = latest_deployment.deployment_action.first()
            if deployment_action.action_type != 'retire':
                deployment_status = deployment_action.action_type
            else:
                deployment_status = None
        return deployment_status
    """
    # get the most recent Deploy to Sea and Recover from Sea action timestamps, add this time delta to the time_at_sea column
    def update_time_at_sea(self):
        try:
            action_deploy_to_sea = BuildAction.objects.filter(build=self).filter(action_type='deploymenttosea').latest('created_at')
        except BuildAction.DoesNotExist:
            action_deploy_to_sea = None

        try:
            action_recover = BuildAction.objects.filter(build=self).filter(action_type='deploymentrecover').latest('created_at')
        except BuildAction.DoesNotExist:
            action_recover = None

        if action_deploy_to_sea and action_recover:
            latest_time_at_sea =  action_recover.created_at - action_deploy_to_sea.created_at
        else:
            latest_time_at_sea = timedelta(minutes=0)

        # add to existing Time at Sea duration
        self.time_at_sea = self.time_at_sea + latest_time_at_sea
        self.save()

    # get the time at sea for the current deployment only (if item is at sea)
    def current_deployment_time_at_sea(self):
        current_deployment_time = timedelta(minutes=0)


        if self.current_deployment() and self.current_deployment().current_deployment_status() == 'deploy':
            try:
                action_deploy_to_sea = BuildAction.objects.filter(build=self).filter(action_type='deploymenttosea').latest('created_at')
            except BuildAction.DoesNotExist:
                action_deploy_to_sea = None

            if action_deploy_to_sea:
                now = timezone.now()
                current_time_at_sea = now - action_deploy_to_sea.created_at
                current_deployment_time = current_time_at_sea

        return current_deployment_time

    # get the Total Time at Sea by adding historical sea time and current deployment sea time
    def total_time_at_sea(self):
        return self.time_at_sea + self.current_deployment_time_at_sea()


class BuildAction(models.Model):
    BUILDADD = 'buildadd'
    LOCATIONCHANGE = 'locationchange'
    SUBASSEMBLYCHANGE = 'subassemblychange'
    STARTDEPLOY = 'startdeploy'
    REMOVEFROMDEPLOYMENT = 'removefromdeployment'
    DEPLOYMENTBURNIN = 'deploymentburnin'
    DEPLOYMENTTOSEA = 'deploymenttosea'
    DEPLOYMENTUPDATE = 'deploymentupdate'
    DEPLOYMENTRECOVER = 'deploymentrecover'
    TEST = 'test'
    NOTE = 'note'
    HISTORYNOTE = 'historynote'
    TICKET = 'ticket'
    FLAG = 'flag'
    RETIREBUILD = 'retirebuild'
    ACT_TYPES = (
        (BUILDADD, 'Add Build'),
        (LOCATIONCHANGE, 'Location Change'),
        (SUBASSEMBLYCHANGE, 'Subassembly Change'),
        (STARTDEPLOY, 'Start Deployment'),
        (REMOVEFROMDEPLOYMENT, 'Deployment Ended'),
        (DEPLOYMENTBURNIN, 'Deployment Burnin'),
        (DEPLOYMENTTOSEA, 'Deployment to Sea'),
        (DEPLOYMENTUPDATE, 'Deployment Update'),
        (DEPLOYMENTRECOVER, 'Deployment Recovered'),
        (TEST, 'Test'),
        (NOTE, 'Note'),
        (HISTORYNOTE, 'Historical Note'),
        (TICKET, 'Work Ticket'),
        (FLAG, 'Flag'),
        (RETIREBUILD, 'Retire Build'),
    )
    action_type = models.CharField(max_length=20, choices=ACT_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    detail = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name='actions',
                             on_delete=models.SET_NULL, null=True, blank=False)
    location = TreeForeignKey(Location, related_name='actions',
                              on_delete=models.SET_NULL, null=True, blank=False)
    build = models.ForeignKey(Build, related_name='actions',
                                 on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at', 'action_type']

    def __str__(self):
        return self.get_action_type_display()


class PhotoNote(models.Model):
    photo = models.FileField(upload_to='notes/',
                             validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'csv'])])
    build = models.ForeignKey(Build, related_name='build_photos',
                                 on_delete=models.CASCADE, null=True, blank=True)
    action = models.ForeignKey(BuildAction, related_name='build_photos',
                                 on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='build_photos',
                             on_delete=models.SET_NULL, null=True, blank=False)

    def file_type(self):
        # get the file extension from file name
        name, extension = os.path.splitext(self.photo.name)
        # set the possible extensions for docs and images
        doc_types = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
        image_types = ['.png', '.jpg', '.jpeg', '.gif']

        if extension in doc_types:
            return 'document'
        if extension in image_types:
            return 'image'
        return 'other'


class BuildSnapshot(models.Model):
    build = models.ForeignKey(Build, related_name='build_snapshots', on_delete=models.CASCADE, null=True, blank=True)
    deployment = models.ForeignKey('inventory.Deployment', related_name='build_snapshots',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    deployment_status = models.CharField(max_length=255, null=False, blank=True)
    location = TreeForeignKey(Location, related_name='build_snapshots',
                              on_delete=models.SET_NULL, null=True, blank=False, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    time_at_sea = models.DurationField(default=timedelta(minutes=0), null=True, blank=True)

    class Meta:
        ordering = ['build', 'deployment', '-created_at']

    def __str__(self):
        return self.build.__str__()


class InventorySnapshot(MPTTModel):
    inventory = models.ForeignKey('inventory.Inventory', related_name='inventory_snapshots',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    parent = TreeForeignKey('self', related_name='children',
                            on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    build = models.ForeignKey(BuildSnapshot, related_name='inventory_snapshots',
                                   on_delete=models.CASCADE, null=True, blank=True)
    location = TreeForeignKey(Location, related_name='inventory_snapshots',
                              on_delete=models.SET_NULL, null=True, blank=False, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    order = models.CharField(max_length=255, null=False, blank=True, db_index=True)

    class MPTTMeta:
        order_insertion_by = ['order']

    def __str__(self):
        return self.inventory.serial_number
