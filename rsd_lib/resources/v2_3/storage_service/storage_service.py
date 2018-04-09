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


class StorageService(base.ResourceBase):

    description = base.Field('Description')
    """The storage service description"""

    identity = base.Field('Id', required=True)
    """The storage service identity string"""

    name = base.Field('Name')
    """The storage service name"""

    status = StatusField('Status')
    """The storage service status"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a StorageService

        :param connector: A Connector instance
        :param identity: The identity of the StorageService resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(StorageService, self).__init__(connector, identity,
                                             redfish_version)


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
