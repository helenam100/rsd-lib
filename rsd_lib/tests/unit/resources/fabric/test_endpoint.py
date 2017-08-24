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

from rsd_lib.resources.fabric import endpoint


class EndpointTestCase(testtools.TestCase):

    def setUp(self):
        super(EndpointTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/endpoint.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.endpoint_inst = endpoint.Endpoint(
            self.conn, '/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.endpoint_inst._parse_attributes()
        self.assertEqual('1.0.2', self.endpoint_inst.redfish_version)
        self.assertEqual('The PCIe Physical function of an 850GB NVMe drive',
                         self.endpoint_inst.description)
        self.assertEqual('NVMeDrivePF1', self.endpoint_inst.identity)
        self.assertEqual('NVMe Drive', self.endpoint_inst.name)
        self.assertEqual(1000, self.endpoint_inst.host_reservation_memory)
        self.assertEqual([], self.endpoint_inst.redundancy)
        self.assertEqual('UUID',
                         self.endpoint_inst.identifiers[0].name_format)
        self.assertEqual('00000000-0000-0000-0000-000000000000',
                         self.endpoint_inst.identifiers[0].name)
        self.assertEqual('Drive',
                         self.endpoint_inst.connected_entities[0].entity_type)
        self.assertEqual('Target',
                         self.endpoint_inst.connected_entities[0].entity_role)
        self.assertEqual('/redfish/v1/Chassis/PCIeSwitch1/Drives/Disk.Bay.0',
                         self.endpoint_inst.connected_entities[0].entity_link)
        self.assertEqual(
            'UUID',
            self.endpoint_inst.connected_entities[0].
            identifiers[0].name_format)
        self.assertEqual(
            '00000000-0000-0000-0000-000000000000',
            self.endpoint_inst.connected_entities[0].identifiers[0].name)


class EndpointCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(EndpointCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'endpoint_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.endpoint_col = endpoint.EndpointCollection(
            self.conn, '/redfish/v1/Fabrics/PCIe/Endpoints',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.endpoint_col._parse_attributes()
        self.assertEqual('1.0.2', self.endpoint_col.redfish_version)
        self.assertEqual('PCIe Endpoint Collection',
                         self.endpoint_col.name)
        self.assertEqual(('/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF1',
                          '/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF2',
                          '/redfish/v1/Fabrics/PCIe/'
                          'Endpoints/HostRootComplex1'),
                         self.endpoint_col.members_identities)

    @mock.patch.object(endpoint, 'Endpoint', autospec=True)
    def test_get_member(self, mock_endpoint):
        self.endpoint_col.get_member(
            '/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF1')
        mock_endpoint.assert_called_once_with(
            self.endpoint_col._conn,
            '/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF1',
            redfish_version=self.endpoint_col.redfish_version)

    @mock.patch.object(endpoint, 'Endpoint', autospec=True)
    def test_get_members(self, mock_endpoint):
        members = self.endpoint_col.get_members()
        mock_endpoint.assert_called_with(
            self.endpoint_col._conn, '/redfish/v1/Fabrics/PCIe/Endpoints'
                                     '/HostRootComplex1',
            redfish_version=self.endpoint_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(3, len(members))
