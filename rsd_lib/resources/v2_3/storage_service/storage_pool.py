# Copyright 2018 Intel, Inc.
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
from sushy import utils

from rsd_lib.resources.v2_3.storage_service import volume
from rsd_lib import utils as rsd_lib_utils


LOG = logging.getLogger(__name__)


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


class CapacityField(base.CompositeField):
    allocated_bytes = base.Field(['Data', 'AllocatedBytes'], adapter=int)
    consumed_bytes = base.Field(['Data', 'ConsumedBytes'], adapter=int)
    guaranteed_bytes = base.Field(['Data', 'GuaranteedBytes'], adapter=int)
    provisioned_bytes = base.Field(['Data', 'ProvisionedBytes'], adapter=int)


class CapacitySourcesField(base.ListField):
    providing_drives = base.Field('ProvidingDrives', default=(),
                                  adapter=utils.get_members_identities)
    provided_capacity = CapacityField('ProvidedCapacity')


class StoragePool(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The storage pool  identity string"""

    description = base.Field('Description')
    """The storage pool  description string"""

    name = base.Field('Name')
    """The storage pool  name string"""

    status = StatusField('Status')
    """The storage pool  status"""

    capacity = CapacityField('Capacity')
    """The storage pool capacity info"""

    capacity_sources = CapacitySourcesField('CapacitySources')
    """The storage pool capacity source info"""

    _allocated_volumes = None  # ref to allocated volumes collection

    _allocated_pools = None  # ref to allocated pools collection

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a LogicalDrive

        :param connector: A Connector instance
        :param identity: The identity of the LogicalDrive resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(StoragePool, self).__init__(connector, identity, redfish_version)

    def _get_allocated_volumes_path(self):
        """Helper function to find the AllocatedVolumes path"""
        volume_col = self.json.get('AllocatedVolumes')
        if not volume_col:
            raise exceptions.MissingAttributeError(
                attribute='AllocatedVolumes', resource=self._path)
        return rsd_lib_utils.get_resource_identity(volume_col)

    @property
    def allocated_volumes(self):
        """Property to provide reference to `AllocatedVolumes` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        if self._allocated_volumes is None:
            self._allocated_volumes = volume.VolumeCollection(
                self._conn, self._get_allocated_volumes_path(),
                redfish_version=self.redfish_version)

        return self._allocated_volumes

    def _get_allocated_pools_path(self):
        """Helper function to find the AllocatedPools path"""
        storage_pool_col = self.json.get('AllocatedPools')
        if not storage_pool_col:
            raise exceptions.MissingAttributeError(
                attribute='AllocatedPools', resource=self._path)
        return rsd_lib_utils.get_resource_identity(storage_pool_col)

    @property
    def allocated_pools(self):
        """Property to provide reference to `AllocatedPools` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        if self._allocated_pools is None:
            self._allocated_pools = StoragePoolCollection(
                self._conn, self._get_allocated_pools_path(),
                redfish_version=self.redfish_version)

        return self._allocated_pools

    def refresh(self):
        super(StoragePool, self).refresh()
        self._allocated_volumes = None
        self._allocated_pools = None


class StoragePoolCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return StoragePool

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a StoragePoolCollection

        :param connector: A Connector instance
        :param path: The canonical path to the StoragePool collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(StoragePoolCollection, self).__init__(connector, path,
                                                    redfish_version)
