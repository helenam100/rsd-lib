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


class IdentifiersField(base.ListField):
    name_format = base.Field('DurableNameFormat')
    name = base.Field('DurableName')


class ConnectedEntitiesField(base.ListField):
    entity_type = base.Field('EntityType')
    entity_role = base.Field('EntityRole')
    entity_link = base.Field('EntityLink',
                             adapter=rsd_lib_utils.get_resource_identity)


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


class LinksField(base.CompositeField):
    ports = base.Field('Ports', adapter=utils.get_members_identities)
    endpoints = base.Field('Endpoints', adapter=utils.get_members_identities)
    zones = base.Field(['Oem', 'Intel_RackScale', 'Zones'],
                       adapter=utils.get_members_identities)
    interface = base.Field(['Oem', 'Intel_RackScale', 'Interface'],
                           adapter=rsd_lib_utils.get_resource_identity)


class IPTransportDetailsField(base.ListField):
    transport_protocol = base.Field('TransportProtocol')
    ipv4_address = base.Field(['IPv4Address', 'Address'])
    ipv6_address = base.Field(['IPv6Address', 'Address'])
    port = base.Field('Port', adapter=int)


class AuthenticationField(base.CompositeField):
    username = base.Field('Username')
    password = base.Field('Password')


class OemField(base.CompositeField):
    authentication = AuthenticationField(['Intel_RackScale', 'Authentication'])


class Endpoint(base.ResourceBase):

    connected_entities = ConnectedEntitiesField('ConnectedEntities')
    """Entities connected to endpoint"""

    description = base.Field('Description')
    """The endpoint description"""

    protocol = base.Field('EndpointProtocol')
    """Protocol for endpoint (i.e. PCIe)"""

    identifiers = IdentifiersField('Identifiers')
    """Identifiers for endpoint"""

    identity = base.Field('Id', required=True)
    """The endpoint identity string"""

    name = base.Field('Name')
    """The endpoint name"""

    status = StatusField('Status')
    """The endpoint status"""

    links = LinksField('Links')
    """These links to related components of this endpoint"""

    ip_transport_details = IPTransportDetailsField('IPTransportDetails')
    """IP transport details info of this endpoint"""

    oem = OemField('Oem')
    """The OEM additional info of this endpoint"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing an Endpoint

        :param connector: A Connector instance
        :param identity: The identity of the RemoteTarget resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Endpoint, self).__init__(connector, identity,
                                       redfish_version)

    def update_authentication(self, username=None, password=None):
        """Update endpoint authentication

        :param username: an endpoint username used to authenticate it on the
                         other side of a communication channel
        :param password: an endpoint password
        :raises: BadRequestError if at least one param isn't specified
        """
        if username is None and password is None:
            raise ValueError('At least "username" or "password" parameter has '
                             'to be specified')

        data = {
            "Oem": {
                "Intel_RackScale": {
                    "@odata.type": "#Intel.Oem.Endpoint",
                    "Authentication": {}
                }
            }
        }
        if username is not None:
            data['Oem']['Intel_RackScale']['Authentication']['Username'] = \
                username
        if password is not None:
            data['Oem']['Intel_RackScale']['Authentication']['Password'] = \
                password

        self._conn.patch(self.path, data=data)


class EndpointCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Endpoint

    def __init__(self, connector, path, redfish_version=None):
        """A class representing an Endpoint

        :param connector: A Connector instance
        :param path: The canonical path to the Endpoint collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(EndpointCollection, self).__init__(connector, path,
                                                 redfish_version)
