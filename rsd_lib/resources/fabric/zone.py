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
from sushy import utils

from rsd_lib.resources.fabric import endpoint

LOG = logging.getLogger(__name__)


class ZoneLinksField(base.CompositeField):
    endpoint_identities = base.Field('Endpoints', default=[],
                                     adapter=utils.get_members_identities)


class Zone(base.ResourceBase):

    description = base.Field('Description')
    """The zone description"""

    identity = base.Field('Id', required=True)
    """The zone identity string"""

    name = base.Field('Name')
    """The zone name"""

    links = ZoneLinksField('Links')
    """The zone links"""

    _endpoints = None  # ref to contained endpoints

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Zone

        :param connector: A Connector instance
        :param identity: The identity of the Zone resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Zone, self).__init__(connector, identity,
                                   redfish_version)

    def get_endpoints(self):
        """Return a list of Endpoints present in the Zone

        :returns: A list of Endpoint objects
        """
        return [endpoint.Endpoint(self._conn, id_, self.redfish_version) for
                id_ in self.links.endpoint_identities]


class ZoneCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Zone

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a Zone Collection

        :param connector: A Connector instance
        :param path: The canonical path to the Zone collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(ZoneCollection, self).__init__(connector, path,
                                             redfish_version)
