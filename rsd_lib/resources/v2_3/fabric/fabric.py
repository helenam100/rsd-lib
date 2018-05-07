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

LOG = logging.getLogger(__name__)


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


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

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Fabric

        :param connector: A Connector instance
        :param identity: The identity of the Fabric resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Fabric, self).__init__(connector, identity,
                                     redfish_version)


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
