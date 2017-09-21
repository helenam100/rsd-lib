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
from sushy import exceptions
import testtools

from rsd_lib.resources.fabric import endpoint
from rsd_lib.resources.fabric import fabric
from rsd_lib.resources.fabric import zone


class FabricTestCase(testtools.TestCase):

    def setUp(self):
        super(FabricTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/fabric.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.fabric_inst = fabric.Fabric(
            self.conn, '/redfish/v1/Fabrics/PCIe',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.fabric_inst._parse_attributes()
        self.assertEqual('1.0.2', self.fabric_inst.redfish_version)
        self.assertEqual('PCIe Fabric', self.fabric_inst.description)
        self.assertEqual('PCIe', self.fabric_inst.identity)
        self.assertEqual('PCIe Fabric', self.fabric_inst.name)
        self.assertEqual('PCIe', self.fabric_inst.fabric_type)
        self.assertEqual(5, self.fabric_inst.max_zones)
        self.assertEqual('Enabled', self.fabric_inst.status.state)
        self.assertEqual('OK', self.fabric_inst.status.health)
        self.assertIsNone(self.fabric_inst._endpoints)
        self.assertIsNone(self.fabric_inst._zones)

    def test__get_endpoint_collection_path_missing_attr(self):
        self.fabric_inst._json.pop('Endpoints')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Endpoints',
            self.fabric_inst._get_endpoint_collection_path)

    def test_endpoints(self):
        # check for the underneath variable value
        self.assertIsNone(self.fabric_inst._endpoints)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'endpoint_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_endpoints = self.fabric_inst.endpoints
        # | THEN |
        self.assertIsInstance(actual_endpoints,
                              endpoint.EndpointCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_endpoints,
                      self.fabric_inst.endpoints)
        self.conn.get.return_value.json.assert_not_called()

    def test_endpoints_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'endpoint_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.fabric_inst.endpoints,
                              endpoint.EndpointCollection)

        # On refreshing the fabric instance...
        with open('rsd_lib/tests/unit/json_samples/'
                  'fabric.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.fabric_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.fabric_inst._endpoints)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'endpoint_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.fabric_inst.endpoints,
                              endpoint.EndpointCollection)

    def test__get_zone_collection_path_missing_attr(self):
        self.fabric_inst._json.pop('Zones')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Zones',
            self.fabric_inst._get_zone_collection_path)

    def test_zones(self):
        # check for the underneath variable value
        self.assertIsNone(self.fabric_inst._zones)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'zone_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_zones = self.fabric_inst.zones
        # | THEN |
        self.assertIsInstance(actual_zones,
                              zone.ZoneCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_zones,
                      self.fabric_inst.zones)
        self.conn.get.return_value.json.assert_not_called()

    def test_zones_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'zone_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.fabric_inst.zones,
                              zone.ZoneCollection)

        # On refreshing the fabric instance...
        with open('rsd_lib/tests/unit/json_samples/'
                  'fabric.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.fabric_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.fabric_inst._zones)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'zone_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.fabric_inst.zones,
                              zone.ZoneCollection)


class FabricCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(FabricCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'fabric_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.fabric_col = fabric.FabricCollection(
            self.conn, '/redfish/v1/Fabrics', redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.fabric_col._parse_attributes()
        self.assertEqual('1.0.2', self.fabric_col.redfish_version)
        self.assertEqual('Fabric Collection',
                         self.fabric_col.name)
        self.assertEqual(('/redfish/v1/Fabrics/PCIe',),
                         self.fabric_col.members_identities)

    @mock.patch.object(fabric, 'Fabric', autospec=True)
    def test_get_member(self, mock_fabric):
        self.fabric_col.get_member('/redfish/v1/Fabrics/PCIe')
        mock_fabric.assert_called_once_with(
            self.fabric_col._conn, '/redfish/v1/Fabrics/PCIe',
            redfish_version=self.fabric_col.redfish_version)

    @mock.patch.object(fabric, 'Fabric', autospec=True)
    def test_get_members(self, mock_fabric):
        members = self.fabric_col.get_members()
        mock_fabric.assert_called_once_with(
            self.fabric_col._conn, '/redfish/v1/Fabrics/PCIe',
            redfish_version=self.fabric_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
