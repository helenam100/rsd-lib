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

import json
import mock
import testtools

from sushy import exceptions

from rsd_lib.resources.v2_3.node import node


class NodeTestCase(testtools.TestCase):

    def setUp(self):
        super(NodeTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/node.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.node_inst = node.Node(
            self.conn, '/redfish/v1/Nodes/Node1',
            redfish_version='1.0.2')

    def test_attach_endpoint(self):
        self.node_inst.attach_endpoint(
            endpoint='/redfish/v1/StorageServices/NVMeoE1/Volumes/1',
            protocol='NVMeOverFabrics')
        self.node_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Nodes/Node1/Actions/ComposedNode.AttachEndpoint',
            data={'Resource': {'@odata.id': '/redfish/v1/'
                               'StorageServices/NVMeoE1/Volumes/1'},
                  'Protocol': 'NVMeOverFabrics'})

    def test_attach_endpoint_invalid_parameter(self):
        self.assertRaises(exceptions.InvalidParameterValueError,
                          self.node_inst.attach_endpoint,
                          endpoint='invalid')

    def test_attach_endpoint_only_with_resource_uri(self):
        self.node_inst.attach_endpoint(
            endpoint='/redfish/v1/StorageServices/NVMeoE1/Volumes/1')
        self.node_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Nodes/Node1/Actions/ComposedNode.AttachEndpoint',
            data={'Resource': {'@odata.id': '/redfish/v1/'
                               'StorageServices/NVMeoE1/Volumes/1'}})
