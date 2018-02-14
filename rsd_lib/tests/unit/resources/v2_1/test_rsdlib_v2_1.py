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

import json
import mock
import testtools

from rsd_lib.resources import v2_1
from rsd_lib.resources.v2_1.chassis import chassis
from rsd_lib.resources.v2_1.fabric import fabric
from rsd_lib.resources.v2_1.node import node
from rsd_lib.resources.v2_1.storage_service import storage_service
from rsd_lib.resources.v2_1.system import system


class RSDLibV2_1TestCase(testtools.TestCase):

    def setUp(self):
        super(RSDLibV2_1TestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/root.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.rsd = v2_1.RSDLibV2_1(self.conn)

    def test__parse_attributes(self):
        self.rsd._parse_attributes()
        self.assertEqual("2.1.0", self.rsd._rsd_api_version)
        self.assertEqual("1.0.2", self.rsd._redfish_version)
        self.assertEqual("/redfish/v1/Systems", self.rsd._systems_path)
        self.assertEqual("/redfish/v1/Nodes", self.rsd._nodes_path)
        self.assertEqual("/redfish/v1/Chassis", self.rsd._chassis_path)
        self.assertEqual("/redfish/v1/Services",
                         self.rsd._storage_service_path)
        self.assertEqual("/redfish/v1/Fabrics", self.rsd._fabrics_path)

    @mock.patch.object(system, 'SystemCollection', autospec=True)
    def test_get_system_collection(self, mock_system_collection):
        self.rsd.get_system_collection()
        mock_system_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Systems',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(system, 'System', autospec=True)
    def test_get_system(self, mock_system):
        self.rsd.get_system('fake-system-id')
        mock_system.assert_called_once_with(
            self.rsd._conn, 'fake-system-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(node, 'NodeCollection', autospec=True)
    def test_get_node_collection(self, mock_node_collection):
        self.rsd.get_node_collection()
        mock_node_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Nodes',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(node, 'Node', autospec=True)
    def test_get_node(self, mock_node):
        self.rsd.get_node('fake-node-id')
        mock_node.assert_called_once_with(
            self.rsd._conn, 'fake-node-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(fabric, 'FabricCollection', autospec=True)
    def test_get_fabric_collection(self, mock_fabric_collection):
        self.rsd.get_fabric_collection()
        mock_fabric_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Fabrics',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(fabric, 'Fabric', autospec=True)
    def test_get_fabric(self, mock_fabric):
        self.rsd.get_fabric('fake-fabric-id')
        mock_fabric.assert_called_once_with(
            self.rsd._conn, 'fake-fabric-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(chassis, 'ChassisCollection', autospec=True)
    def test_get_chassis_collection(self, mock_chassis_collection):
        self.rsd.get_chassis_collection()
        mock_chassis_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Chassis',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(chassis, 'Chassis', autospec=True)
    def test_get_chassis(self, mock_chassis):
        self.rsd.get_chassis('fake-chassis-id')
        mock_chassis.assert_called_once_with(
            self.rsd._conn, 'fake-chassis-id',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(storage_service, 'StorageServiceCollection',
                       autospec=True)
    def test_get_storage_service_collection(self,
                                            mock_storage_service_collection):
        self.rsd.get_storage_service_collection()
        mock_storage_service_collection.assert_called_once_with(
            self.rsd._conn, '/redfish/v1/Services',
            redfish_version=self.rsd.redfish_version)

    @mock.patch.object(storage_service, 'StorageService', autospec=True)
    def test_get_storage_service(self, mock_storage_service):
        self.rsd.get_storage_service('fake-storage-service-id')
        mock_storage_service.assert_called_once_with(
            self.rsd._conn, 'fake-storage-service-id',
            redfish_version=self.rsd.redfish_version)
