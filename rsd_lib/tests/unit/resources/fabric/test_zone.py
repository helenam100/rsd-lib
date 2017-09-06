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

from rsd_lib.resources.fabric import zone


class ZoneTestCase(testtools.TestCase):

    def setUp(self):
        super(ZoneTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/zone.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.zone_inst = zone.Zone(
            self.conn, '/redfish/v1/Fabrics/PCIe/Zones/1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.zone_inst._parse_attributes()
        self.assertEqual('1.0.2', self.zone_inst.redfish_version)
        self.assertEqual('PCIe Zone 1',
                         self.zone_inst.description)
        self.assertEqual('1', self.zone_inst.identity)
        self.assertEqual('PCIe Zone 1', self.zone_inst.name)
        self.assertEqual(('/redfish/v1/Fabrics/PCIe/'
                          'Endpoints/HostRootComplex1',
                          '/redfish/v1/Fabrics/PCIe/Endpoints/NVMeDrivePF2'),
                         self.zone_inst.links.endpoint_identities)

    def test_get_endpoints(self):
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/endpoint.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        endpoints = self.zone_inst.get_endpoints()
        self.assertEqual(endpoints[0].identity, 'NVMeDrivePF1')


class ZoneCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(ZoneCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'zone_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.zone_col = zone.ZoneCollection(
            self.conn, '/redfish/v1/Fabrics/PCIe/Zones',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.zone_col._parse_attributes()
        self.assertEqual('1.0.2', self.zone_col.redfish_version)
        self.assertEqual('PCIe Zone Collection',
                         self.zone_col.name)
        self.assertEqual(('/redfish/v1/Fabrics/PCIe/Zones/1',
                          '/redfish/v1/Fabrics/PCIe/Zones/2'),
                         self.zone_col.members_identities)

    @mock.patch.object(zone, 'Zone', autospec=True)
    def test_get_member(self, mock_zone):
        self.zone_col.get_member('/redfish/v1/Fabrics/PCIe/Zones/1')
        mock_zone.assert_called_once_with(
            self.zone_col._conn, '/redfish/v1/Fabrics/PCIe/Zones/1',
            redfish_version=self.zone_col.redfish_version)

    @mock.patch.object(zone, 'Zone', autospec=True)
    def test_get_members(self, mock_zone):
        members = self.zone_col.get_members()
        mock_zone.assert_called_with(
            self.zone_col._conn, '/redfish/v1/Fabrics/PCIe/Zones/2',
            redfish_version=self.zone_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))
