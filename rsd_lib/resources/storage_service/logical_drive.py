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

LOG = logging.getLogger(__name__)


class LogicalDrive(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The logical drive identity string"""

    drive_type = base.Field('Type')
    """Type of logical drive"""

    mode = base.Field('Mode')
    """Drive mode - for Type=='LVM' only supported mode is 'LV'"""

    protected = base.Field('Protected')
    """If logical drive is protected"""

    capacity_gib = base.Field('CapacityGiB')
    """Logical drive capacity in GiB"""

    image = base.Field('Image')
    """Any name that identifies the content of image copied to this LV"""

    bootable = base.Field('Bootable')
    """If the LV contains a bootable operating system"""

    snapshot = base.Field('Snapshot')
    """Type of drive replication. Yes - copy on write, No - disc clone"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a LogicalDrive

        :param connector: A Connector instance
        :param identity: The identity of the LogicalDrive resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(LogicalDrive, self).__init__(connector, identity,
                                           redfish_version)


class LogicalDriveCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return LogicalDrive

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a LogicalDriveCollection

        :param connector: A Connector instance
        :param path: The canonical path to the LogicalDrive collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(LogicalDriveCollection, self).__init__(connector, path,
                                                     redfish_version)
