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

from sushy.resources import base


class MemoryLocationField(base.CompositeField):
    socket = base.Field('Socket', required=int)
    memory_controller = base.Field('MemoryController', required=int)
    channel = base.Field('Channel', required=int)
    slot = base.Field('Slot', required=int)


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


class Memory(base.ResourceBase):

    name = base.Field('Name')
    """The memory name"""

    identity = base.Field('Id', required=True)
    """The memory identity string"""

    memory_type = base.Field('MemoryType')
    """The type of memory"""

    memory_device_type = base.Field('MemoryDeviceType')
    """The type of memory device"""

    base_module_type = base.Field('BaseModuleType')
    """The type of base module"""

    memory_media = base.Field('MemoryMedia', adapter=list)
    """The memory media"""

    capacity_mib = base.Field('CapacityMiB', adapter=int)
    """The capacity of this memory in MiB"""

    data_width_bits = base.Field('DataWidthBits', adapter=int)
    """The data width bits of this memory."""

    bus_width_bits = base.Field('BusWidthBits', adapter=int)
    """The bus width bits of this memory."""

    manufacturer = base.Field('Manufacturer')
    """The manufacturer of this memory"""

    serial_number = base.Field('SerialNumber')
    """The serial number of this memory"""

    part_number = base.Field('PartNumber')
    """The part number of this memory"""

    allowed_speeds_mhz = base.Field('AllowedSpeedsMHz', adapter=list)
    """The allowed speeds of this memory in MHz"""

    firmware_revision = base.Field('FirmwareRevision')
    """The revision of this memory firmware"""

    frirmware_api_version = base.Field('FirmwareApiVersion')
    """The API revision of this memory firmware"""

    function_classes = base.Field('FunctionClasses', adapter=list)
    """The function_classes  of the memory"""

    vendor_id = base.Field('VendorID')
    """The vendor identity"""

    device_id = base.Field('DeviceID')
    """The device identity"""

    rank_count = base.Field('RankCount', adapter=int)
    """The rank count of this memory"""

    device_locator = base.Field('DeviceLocator')
    """The device locator"""

    error_correction = base.Field('ErrorCorrection')
    """The error correction"""

    operating_speed_mhz = base.Field('OperatingSpeedMhz', adapter=int)
    """The operating speed of this memory in MHz"""

    operating_memory_modes = base.Field('OperatingMemoryModes', adapter=list)
    """The operating memory modes"""

    memory_location = MemoryLocationField('MemoryLocation')
    """The location information of this memory"""

    status = StatusField('Status')
    """The memory status"""

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Processor

        :param connector: A Connector instance
        :param identity: The identity of the processor
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Memory, self).__init__(connector, identity, redfish_version)


class MemoryCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Memory

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a ProcessorCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Processor collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(MemoryCollection, self).__init__(connector, path,
                                               redfish_version)
