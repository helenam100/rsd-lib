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

from sushy.resources import base

from rsd_lib.resources import base as rsd_base
from rsd_lib import utils

LOG = logging.getLogger(__name__)


class IdentifiersField(rsd_base.FieldList):
    name_format = base.Field('DurableNameFormat')
    name = base.Field('DurableName')


class EntityLinkField(base.CompositeField):
    # TODO(ntpttr): Link to the actual object once we have a class for it.
    identity = base.Field('@odata.id')


class ConnectedEntitiesField(rsd_base.FieldList):
    entity_type = base.Field('EntityType')
    entity_role = base.Field('EntityRole')
    entity_link = base.Field('EntityLink',
                             adapter=utils.get_resource_identity)
    identifiers = IdentifiersField('Identifiers')


class Endpoint(base.ResourceBase):

    connected_entities = ConnectedEntitiesField('ConnectedEntities')
    """Entities connected to endpoint"""

    description = base.Field('Description')
    """The endpoint description"""

    host_reservation_memory = base.Field('HostReservationMemoryBytes')
    """Host reservation memory in bytes"""

    protocol = base.Field('EndpointProtocol')
    """Protocol for endpoint (i.e. PCIe)"""

    identifiers = IdentifiersField('Identifiers')
    """Identifiers for endpoint"""

    identity = base.Field('Id', required=True)
    """The endpoint identity string"""

    name = base.Field('Name')
    """The endpoint name"""

    redundancy = base.Field('Redundancy')
    """The endpoint redundancy"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing an Endpoint

        :param connector: A Connector instance
        :param identity: The identity of the RemoteTarget resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Endpoint, self).__init__(connector, identity,
                                       redfish_version)


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
