# Copyright 2017 Intel, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from sushy import exceptions
from sushy.resources import base

from rsd_lib.resources.storage_service import logical_drive
from rsd_lib.resources.storage_service import physical_drive
from rsd_lib.resources.storage_service import remote_target

LOG = logging.getLogger(__name__)


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')


class StorageService(base.ResourceBase):

    description = base.Field('Description')
    """The storage service description"""

    identity = base.Field('Id', required=True)
    """The storage service identity string"""

    name = base.Field('Name')
    """The storage service name"""

    status = StatusField('Status')
    """The storage service status"""

    _logical_drives = None  # ref to LogicalDriveCollection instance

    _physical_drives = None  # ref to PhysicalDrivesCollection instance

    _remote_targets = None  # ref to RemoteTargetCollection instance

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a StorageService

        :param connector: A Connector instance
        :param identity: The identity of the StorageService resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(StorageService, self).__init__(connector, identity,
                                             redfish_version)

    def _get_logical_drive_collection_path(self):
        """Helper function to find the LogicalDriveCollection path"""
        logical_drive_col = self.json.get('LogicalDrives')
        if not logical_drive_col:
            raise exceptions.MissingAttributeError(attribute='LogicalDrives',
                                                   resource=self._path)
        return logical_drive_col.get('@odata.id')

    @property
    def logical_drives(self):
        """Property to provide reference to `LogicalDriveCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        if self._logical_drives is None:
            self._logical_drives = logical_drive.LogicalDriveCollection(
                self._conn, self._get_logical_drive_collection_path(),
                redfish_version=self.redfish_version)

        return self._logical_drives

    def _get_physical_drive_collection_path(self):
        """Helper function to find the PhysicalDriveCollection path"""
        physical_drive_col = self.json.get('Drives')
        if not physical_drive_col:
            raise exceptions.MissingAttributeError(attribute='PhysicalDrives',
                                                   resource=self._path)
        return physical_drive_col.get('@odata.id')

    @property
    def physical_drives(self):
        """Property to provide reference to `PhysicalDriveCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        if self._physical_drives is None:
            self._physical_drives = physical_drive.PhysicalDriveCollection(
                self._conn, self._get_physical_drive_collection_path(),
                redfish_version=self.redfish_version)

        return self._physical_drives

    def _get_remote_target_collection_path(self):
        """Helper function to find the RemoteTargetCollection path"""
        remote_target_col = self.json.get('RemoteTargets')
        if not remote_target_col:
            raise exceptions.MissingAttributeError(attribute='RemoteTargets',
                                                   resource=self._path)
        return remote_target_col.get('@odata.id')

    @property
    def remote_targets(self):
        """Property to provide reference to `RemoteTargetCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        if self._remote_targets is None:
            self._remote_targets = remote_target.RemoteTargetCollection(
                self._conn, self._get_remote_target_collection_path(),
                redfish_version=self.redfish_version)

        return self._remote_targets

    def refresh(self):
        super(StorageService, self).refresh()
        self._logical_drives = None
        self._physical_drives = None
        self._remote_targets = None


class StorageServiceCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return StorageService

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a StorageServiceCollection

        :param connector: A Connector instance
        :param path: The canonical path to the StorageService collection
            resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(StorageServiceCollection, self).__init__(connector, path,
                                                       redfish_version)
