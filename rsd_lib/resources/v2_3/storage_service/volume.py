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

from sushy.resources import base
from sushy import utils

from rsd_lib import utils as rsd_lib_utils

LOG = logging.getLogger(__name__)


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


class CapacitySourcesField(base.ListField):
    providing_pools = base.Field('ProvidingPools',
                                 adapter=utils.get_members_identities)
    allocated_Bytes = base.Field(
        ['ProvidedCapacity', 'Data', 'AllocatedBytes'], adapter=int)


class LinksField(base.CompositeField):
    endpoints = base.Field(['Oem', 'Intel_RackScale', 'Endpoints'], default=(),
                           adapter=utils.get_members_identities)
    """Link to related endpoints of this volume"""

    metrics = base.Field(['Oem', 'Intel_RackScale', 'Metrics'],
                         adapter=rsd_lib_utils.get_resource_identity)
    """Link to telemetry metrics of this volume"""


class ReplicaInfosField(base.ListField):
    replica_readonly_access = base.Field('ReplicaReadOnlyAccess')
    replica_type = base.Field('ReplicaType')
    replica_role = base.Field('ReplicaRole')
    replica = base.Field('Replica',
                         adapter=rsd_lib_utils.get_resource_identity)


class Volume(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The volume identity string"""

    description = base.Field('Description')
    """The volume description string"""

    name = base.Field('Name')
    """The volume name string"""

    model = base.Field('Model')
    """The volume model"""

    manufacturer = base.Field('Manufacturer')
    """The volume manufacturer"""

    access_capabilities = base.Field('AccessCapabilities', adapter=list)
    """The access capabilities of volume"""

    capacity_bytes = base.Field('CapacityBytes', adapter=int)
    """The capacity of volume in bytes"""

    allocated_Bytes = base.Field(['Capacity', 'Data', 'AllocatedBytes'],
                                 adapter=int)
    """The allocated capacity of volume in bytes"""

    capacity_sources = CapacitySourcesField('CapacitySources')
    """The logical drive status"""

    links = LinksField('Links')
    """These links to related components of this volume"""

    replica_infos = ReplicaInfosField('ReplicaInfos')
    """These replica related info of this volume"""

    status = StatusField('Status')
    """The volume status"""

    bootable = base.Field(['Oem', 'Intel_RackScale', 'Bootable'], adapter=bool)
    """The bootable info of this volume"""

    erased = base.Field(['Oem', 'Intel_RackScale', 'Erased'])
    """The erased info of this volume"""

    erase_on_detach = base.Field(['Oem', 'Intel_RackScale', 'EraseOnDetach'],
                                 adapter=bool)
    """The rrase on detach info of this volume"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a LogicalDrive

        :param connector: A Connector instance
        :param identity: The identity of the LogicalDrive resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Volume, self).__init__(connector, identity, redfish_version)


class VolumeCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Volume

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a ProcessorCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Processor collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(VolumeCollection, self).__init__(connector, path,
                                               redfish_version)
