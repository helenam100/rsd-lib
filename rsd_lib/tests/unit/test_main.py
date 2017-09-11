# Copyright 2017 Red Hat, Inc.
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
from sushy import connector
import testtools

from rsd_lib import main
from rsd_lib.resources.fabric import fabric
from rsd_lib.resources.node import node


class RSDLibTestCase(testtools.TestCase):

    @mock.patch.object(connector, 'Connector', autospec=True)
    def setUp(self, mock_connector):
        super(RSDLibTestCase, self).setUp()
        self.conn = mock.Mock()
        mock_connector.return_value = self.conn
        with open('rsd_lib/tests/unit/json_samples/root.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.rsd = main.RSDLib('http://foo.bar:8442', username='foo',
                               password='bar', verify=True)

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
