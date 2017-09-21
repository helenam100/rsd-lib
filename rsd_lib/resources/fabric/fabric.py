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

from rsd_lib.resources.fabric import endpoint
from rsd_lib.resources.fabric import zone

LOG = logging.getLogger(__name__)


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')


class Fabric(base.ResourceBase):

    description = base.Field('Description')
    """The fabric description"""

    fabric_type = base.Field('FabricType')
    """The fabric type"""

    identity = base.Field('Id', required=True)
    """The fabric identity string"""

    max_zones = base.Field('MaxZones')
    """Maximum number of zones for the fabric"""

    name = base.Field('Name')
    """The fabric name"""

    status = StatusField('Status')

    _endpoints = None  # ref to EndpointCollection instance

    _zones = None  # ref to ZoneCollection instance

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Fabric

        :param connector: A Connector instance
        :param identity: The identity of the Fabric resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Fabric, self).__init__(connector, identity,
                                     redfish_version)

    def _get_endpoint_collection_path(self):
        """Helper function to find the EndpointCollection path"""
        endpoint_col = self.json.get('Endpoints')
        if not endpoint_col:
            raise exceptions.MissingAttributeError(attribute='Endpoints',
                                                   resource=self._path)
        return endpoint_col.get('@odata.id')

    @property
    def endpoints(self):
        """Property to provide reference to `EndpointCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        if self._endpoints is None:
            self._endpoints = endpoint.EndpointCollection(
                self._conn, self._get_endpoint_collection_path(),
                redfish_version=self.redfish_version)

        return self._endpoints

    def _get_zone_collection_path(self):
        """Helper function to find the ZoneCollection path"""
        zone_col = self.json.get('Zones')
        if not zone_col:
            raise exceptions.MissingAttributeError(attribute='Zones',
                                                   resource=self._path)
        return zone_col.get('@odata.id')

    @property
    def zones(self):
        """Property to provide reference to `ZoneCollection` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        if self._zones is None:
            self._zones = zone.ZoneCollection(
                self._conn, self._get_zone_collection_path(),
                redfish_version=self.redfish_version)

        return self._zones

    def refresh(self):
        super(Fabric, self).refresh()
        self._endpoints = None
        self._zones = None


class FabricCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Fabric

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a FabricCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Fabric collection
            resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(FabricCollection, self).__init__(connector, path,
                                               redfish_version)
