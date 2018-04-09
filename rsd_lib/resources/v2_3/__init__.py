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

from rsd_lib.resources import v2_2
from rsd_lib.resources.v2_3.node import node
from rsd_lib.resources.v2_3.storage_service import storage_service


class RSDLibV2_3(v2_2.RSDLibV2_2):

    # Override telemetry variable inherited from v2.2. The corresponding
    # service don't exist in RSD v2.3
    _telemetry_service_path = None

    _storage_service_path = base.Field(['StorageServices',
                                        '@odata.id'], required=True)
    """StorageServiceCollection path"""

    def get_node(self, identity):
        """Given the identity return a Node object

        :param identity: The identity of the Node resource
        :returns: The Node object
        """
        return node.Node(self._conn, identity,
                         redfish_version=self.redfish_version)

    def get_storage_service_collection(self):
        """Get the StorageServiceCollection object

        :raises: MissingAttributeError, if the collection attribute is
            not found
        :returns: a StorageServiceCollection object
        """
        return storage_service.StorageServiceCollection(
            self._conn, self._storage_service_path,
            redfish_version=self.redfish_version)

    def get_storage_service(self, identity):
        """Given the identity return a StorageService object

        :param identity: The identity of the StorageService resource
        :returns: The StorageService object
        """
        return storage_service.StorageService(
            self._conn, identity,
            redfish_version=self.redfish_version)
