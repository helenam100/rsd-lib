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


class LinksField(base.CompositeField):
    chassis = base.Field('Chassis',
                         adapter=rsd_lib_utils.get_resource_identity)
    """Link to related chassis of this drive"""

    volumes = base.Field('Volumes', default=(),
                         adapter=utils.get_members_identities)
    """Link to related volumes of this drive"""

    endpoints = base.Field('Endpoints', default=(),
                           adapter=utils.get_members_identities)
    """Link to related endpoints of this drive"""


class OemField(base.CompositeField):
    erased = base.Field(['Intel_RackScale', 'DriveErased'], adapter=bool,
                        required=True)
    erase_on_detach = base.Field(['Intel_RackScale', 'EraseOnDetach'],
                                 adapter=bool)
    firmware_version = base.Field(['Intel_RackScale', 'FirmwareVersion'])
    storage = base.Field(['Intel_RackScale', 'Storage'])
    pcie_function = base.Field(['Intel_RackScale', 'PCIeFunction'])


class IdentifiersField(base.ListField):
    durable_name = base.Field('DurableName')
    durable_name_format = base.Field('DurableNameFormat')


class LocationField(base.ListField):
    info = base.Field('Info')
    info_format = base.Field('InfoFormat')


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


class Drive(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The drive identity string"""

    name = base.Field('Name')
    """The drive name string"""

    protocol = base.Field('Protocol')
    """The protocol of this drive"""

    drive_type = base.Field('Type')
    """The protocol of this drive"""

    media_type = base.Field('MediaType')
    """The media type of this drive"""

    capacity_bytes = base.Field('CapacityBytes', adapter=int)
    """The capacity in Bytes of this drive"""

    manufacturer = base.Field('Manufacturer')
    """The manufacturer of this drive"""

    model = base.Field('Model')
    """The drive model"""

    revision = base.Field('Revision')
    """The revision of this drive"""

    sku = base.Field('SKU')
    """The sku of this drive"""

    serial_number = base.Field('SerialNumber')
    """The serial number of this drive"""

    part_number = base.Field('PartNumber')
    """The part number of this drive"""

    asset_tag = base.Field('AssetTag')
    """The asset tag of this drive"""

    rotation_speed_rpm = base.Field('RotationSpeedRPM')
    """The rotation speed of this drive"""

    identifiers = IdentifiersField('Identifiers')
    """These identifiers list of this drive"""

    location = LocationField('Location')
    """The location of this drive"""

    status = StatusField('Status')
    """The drive status"""

    oem = OemField('Oem')
    """The OEM additional info of this drive"""

    status_indicator = base.Field('StatusIndicator')
    """The status indicator state for the status indicator associated
       with this drive"""

    indicator_led = base.Field('IndicatorLED')
    """The indicator light state for the indicator light associated
       with the drive"""

    capable_speed_gbs = base.Field('CapableSpeedGbs')
    """The current bus speed of the associated drive"""

    negotiated_speed_gbs = base.Field('NegotiatedSpeedGbs')
    """The current bus speed of the associated drive"""

    predicted_media_life_left_percent = base.Field(
        'PredictedMediaLifeLeftPercent')
    """An indicator of the percentage of life remaining in the drive's media"""

    links = LinksField('Links')
    """These links to related components of this volume"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Volume

        :param connector: A Connector instance
        :param identity: The identity of the Volume resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Drive, self).__init__(connector, identity, redfish_version)


class DriveCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Drive

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a DriveCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Drive collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(DriveCollection, self).__init__(connector, path,
                                              redfish_version)
