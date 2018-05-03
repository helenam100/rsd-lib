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

import jsonschema
import logging

from sushy import exceptions
from sushy.resources import base
from sushy import utils

from rsd_lib.resources.v2_3.storage_service import volume_schemas
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


class IdentifiersField(base.ListField):
    durable_name = base.Field('DurableName')
    durable_name_format = base.Field('DurableNameFormat')


class ReplicaInfosField(base.ListField):
    replica_readonly_access = base.Field('ReplicaReadOnlyAccess')
    replica_type = base.Field('ReplicaType')
    replica_role = base.Field('ReplicaRole')
    replica = base.Field('Replica',
                         adapter=rsd_lib_utils.get_resource_identity)


class InitializeActionField(base.CompositeField):
    target_uri = base.Field('target', required=True)


class VolumeActionsField(base.CompositeField):
    initialize = InitializeActionField('#Volume.Initialize')


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

    identifiers = IdentifiersField('Identifiers')
    """These identifiers list of this volume"""

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

    _actions = VolumeActionsField('Actions', required=True)

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a LogicalDrive

        :param connector: A Connector instance
        :param identity: The identity of the LogicalDrive resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Volume, self).__init__(connector, identity, redfish_version)

    def update(self, bootable=None, erased=None):
        """Update volume properties

        :param bootable: Change bootable ability of the volume
        :param erased: Provide information if the drive was erased
        :raises: BadRequestError if at least one param isn't specified
        """
        if bootable is None and erased is None:
            raise ValueError('At least "bootable" or "erased" parameter has '
                             'to be specified')

        if bootable and not isinstance(bootable, bool):
            raise exceptions.InvalidParameterValueError(
                parameter='bootable', value=bootable,
                valid_values=[True, False])

        if erased and not isinstance(erased, bool):
            raise exceptions.InvalidParameterValueError(
                parameter='erased', value=erased,
                valid_values=[True, False])

        data = {'Oem': {'Intel_RackScale': {}}}
        if bootable is not None:
            data['Oem']['Intel_RackScale']['Bootable'] = bootable
        if erased is not None:
            data['Oem']['Intel_RackScale']['Erased'] = erased

        self._conn.patch(self.path, data=data)

    def _get_initialize_action_element(self):
        initialize_action = self._actions.initialize
        if not initialize_action:
            raise exceptions.MissingActionError(
                action='#Volume.Initialize',
                resource=self._path)
        return initialize_action

    def initialize(self, init_type):
        """Change initialize type of this volume

        :param type: volume initialize type
        :raises: InvalidParameterValueError if invalid "type" parameter
        """
        allowed_init_type_values = ['Fast', 'Slow']
        if init_type not in allowed_init_type_values:
            raise exceptions.InvalidParameterValueError(
                parameter='init_type', value=init_type,
                valid_values=allowed_init_type_values)

        data = {"InitializeType": init_type}

        target_uri = self._get_initialize_action_element().target_uri
        self._conn.post(target_uri, data=data)

    def delete(self):
        """Delete this volume"""
        self._conn.delete(self.path)


class VolumeCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Volume

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a VolumeCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Volume collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(VolumeCollection, self).__init__(connector, path,
                                               redfish_version)

    def _create_volume_request(self, capacity, access_capabilities=None,
                               capacity_sources=None, replica_infos=None,
                               bootable=None):

        request = {}

        jsonschema.validate(capacity,
                            volume_schemas.capacity_req_schema)
        request['CapacityBytes'] = capacity

        if access_capabilities is not None:
            jsonschema.validate(
                access_capabilities,
                volume_schemas.access_capabilities_req_schema)
            request['AccessCapabilities'] = access_capabilities

        if capacity_sources is not None:
            jsonschema.validate(capacity_sources,
                                volume_schemas.capacity_sources_req_schema)
            request['CapacitySources'] = capacity_sources

        if replica_infos is not None:
            jsonschema.validate(replica_infos,
                                volume_schemas.replica_infos_req_schema)
            request['ReplicaInfos'] = replica_infos

        if bootable is not None:
            jsonschema.validate(bootable,
                                volume_schemas.bootable_req_schema)
            request['Oem'] = {"Intel_RackScale": {"Bootable": bootable}}

        return request

    def create_volume(self, capacity, access_capabilities=None,
                      capacity_sources=None, replica_infos=None,
                      bootable=None):
        """Compose a node from RackScale hardware

        :param capacity: Requested volume capacity in bytes
        :param access_capabilities: List of volume access capabilities
        :param capacity_sources: JSON for volume providing source
        :param replica_infos: JSON for volume replica infos
        :param bootable: Determines if the volume should be bootable
        :returns: The uri of the new volume
        """
        properties = self._create_volume_request(
            capacity=capacity, access_capabilities=access_capabilities,
            capacity_sources=capacity_sources, replica_infos=replica_infos,
            bootable=bootable)
        resp = self._conn.post(self._path, data=properties)
        LOG.info("Volume created at %s", resp.headers['Location'])
        volume_url = resp.headers['Location']
        return volume_url[volume_url.find(self._path):]
