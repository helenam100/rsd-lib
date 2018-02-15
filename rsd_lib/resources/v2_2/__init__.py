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

from rsd_lib.resources import v2_1
from rsd_lib.resources.v2_2.system import system
from rsd_lib.resources.v2_2.telemetry import telemetry


class RSDLibV2_2(v2_1.RSDLibV2_1):

    _nodes_path = base.Field(['Oem', 'Intel_RackScale', 'Nodes', '@odata.id'],
                             required=True)
    """NodeCollection path"""

    _storage_service_path = base.Field(['Oem', 'Intel_RackScale', 'Services',
                                        '@odata.id'], required=True)
    """StorageServiceCollection path"""

    _telemetry_service_path = base.Field(['TelemetryService', '@odata.id'],
                                         required=True)
    """Telemetry Service path"""

    def get_system(self, identity):
        """Given the identity return a System object

        :param identity: The identity of the System resource
        :returns: The System object
        """
        return system.System(self._conn, identity,
                             redfish_version=self.redfish_version)

    def get_system_collection(self):
        """Get the SystemCollection object

        :raises: MissingAttributeError, if the collection attribute is
            not found
        :returns: a SystemCollection object
        """
        return system.SystemCollection(self._conn, self._systems_path,
                                       redfish_version=self.redfish_version)

    def get_telemetry_service(self):
        """Given the identity return a Telemetry Service object

        :param identity: The identity of the Telemetry Service resource
        :returns: The Telemetry Service object
        """
        return telemetry.Telemetry(self._conn, self._telemetry_service_path,
                                   redfish_version=self.redfish_version)
