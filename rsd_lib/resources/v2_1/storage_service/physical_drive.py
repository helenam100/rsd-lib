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


class PhysicalDrive(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The physical drive identity string"""

    interface = base.Field('Interface')
    """The interface for the physical drive"""

    capacity_gib = base.Field('CapacityGiB')
    """Physical drive capacity in GiB"""

    drive_type = base.Field('Type')
    """Type of physical drive"""

    rpm = base.Field('RPM')
    """The RPM of this physical drive"""

    manufacturer = base.Field('Manufacture')
    """The manufacturer of the physical drive"""

    model = base.Field('Model')
    """The model of this physical drive"""

    serial_number = base.Field('SerialNumber')
    """The serial number for the physical drive"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a PhysicalDrive

        :param connector: A Connector instance
        :param identity: The identity of the PhysicalDrive resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(PhysicalDrive, self).__init__(connector, identity,
                                            redfish_version)


class PhysicalDriveCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return PhysicalDrive

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a PhysicalDriveCollection

        :param connector: A Connector instance
        :param path: The canonical path to the PhysicalDrive collection
            resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(PhysicalDriveCollection, self).__init__(connector, path,
                                                      redfish_version)
