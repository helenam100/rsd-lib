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

from rsd_lib.resources.v2_3.fabric import fabric


class FabricTestCase(testtools.TestCase):

    def setUp(self):
        super(FabricTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/fabric.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.fabric_inst = fabric.Fabric(
            self.conn, '/redfish/v1/Fabrics/NVMeoE',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.fabric_inst._parse_attributes()
        self.assertEqual('1.0.2', self.fabric_inst.redfish_version)
        self.assertEqual('NVMeoE', self.fabric_inst.identity)
        self.assertEqual(None, self.fabric_inst.name)
        self.assertEqual('NVMeOverFabrics', self.fabric_inst.fabric_type)
        self.assertEqual(None, self.fabric_inst.max_zones)
        self.assertEqual('Enabled', self.fabric_inst.status.state)
        self.assertEqual('OK', self.fabric_inst.status.health)
        self.assertEqual('OK', self.fabric_inst.status.health_rollup)


class FabricCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(FabricCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'fabric_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.fabric_col = fabric.FabricCollection(
            self.conn, '/redfish/v1/Fabrics', redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.fabric_col._parse_attributes()
        self.assertEqual('1.0.2', self.fabric_col.redfish_version)
        self.assertEqual('Fabric Collection',
                         self.fabric_col.name)
        self.assertEqual(('/redfish/v1/Fabrics/NVMeoE',),
                         self.fabric_col.members_identities)

    @mock.patch.object(fabric, 'Fabric', autospec=True)
    def test_get_member(self, mock_fabric):
        self.fabric_col.get_member('/redfish/v1/Fabrics/NVMeoE')
        mock_fabric.assert_called_once_with(
            self.fabric_col._conn, '/redfish/v1/Fabrics/NVMeoE',
            redfish_version=self.fabric_col.redfish_version)

    @mock.patch.object(fabric, 'Fabric', autospec=True)
    def test_get_members(self, mock_fabric):
        members = self.fabric_col.get_members()
        mock_fabric.assert_called_once_with(
            self.fabric_col._conn, '/redfish/v1/Fabrics/NVMeoE',
            redfish_version=self.fabric_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
