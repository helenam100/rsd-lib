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

from rsd_lib.resources.v2_3.storage_service import drive


class DriveTestCase(testtools.TestCase):

    def setUp(self):
        super(DriveTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/drive.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.drive_inst = drive.Drive(
            self.conn, '/redfish/v1/Chassis/1/Drives/1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.drive_inst._parse_attributes()
        self.assertEqual('1.0.2', self.drive_inst.redfish_version)
        self.assertEqual('2', self.drive_inst.identity)
        self.assertEqual('Physical Drive', self.drive_inst.name)
        self.assertEqual('2', self.drive_inst.identity)
        self.assertEqual('NVMe', self.drive_inst.protocol)
        self.assertEqual('NVMe', self.drive_inst.drive_type)
        self.assertEqual('SSD', self.drive_inst.media_type)
        self.assertEqual(2442408680913, self.drive_inst.capacity_bytes)
        self.assertEqual('Intel Corporation', self.drive_inst.manufacturer)
        self.assertEqual('E323', self.drive_inst.model)
        self.assertEqual(None, self.drive_inst.revision)
        self.assertEqual(None, self.drive_inst.sku)
        self.assertEqual('123fed3029c-b23394-121',
                         self.drive_inst.serial_number)
        self.assertEqual(None, self.drive_inst.part_number)
        self.assertEqual(None, self.drive_inst.asset_tag)
        self.assertEqual(None, self.drive_inst.rotation_speed_rpm)
        self.assertEqual('397f9b78-7e94-11e7-9ea4-001e67dfa170',
                         self.drive_inst.identifiers[0].durable_name)
        self.assertEqual('UUID',
                         self.drive_inst.identifiers[0].durable_name_format)
        self.assertEqual('3', self.drive_inst.location[0].info)
        self.assertEqual('DriveBay number',
                         self.drive_inst.location[0].info_format)
        self.assertEqual('Enabled', self.drive_inst.status.state)
        self.assertEqual('OK', self.drive_inst.status.health)
        self.assertEqual('OK', self.drive_inst.status.health_rollup)
        self.assertEqual(False, self.drive_inst.oem.erased)
        self.assertEqual(True, self.drive_inst.oem.erase_on_detach)
        self.assertEqual('1.0', self.drive_inst.oem.firmware_version)
        self.assertEqual(None, self.drive_inst.oem.storage)
        self.assertEqual(None, self.drive_inst.oem.pcie_function)
        self.assertEqual(None, self.drive_inst.status_indicator)
        self.assertEqual(None, self.drive_inst.indicator_led)
        self.assertEqual(None, self.drive_inst.capable_speed_gbs)
        self.assertEqual(None, self.drive_inst.negotiated_speed_gbs)
        self.assertEqual(95, self.drive_inst.predicted_media_life_left_percent)
        self.assertEqual('/redfish/v1/Chassis/1',
                         self.drive_inst.links.chassis)
        self.assertEqual((), self.drive_inst.links.volumes)
        self.assertEqual((), self.drive_inst.links.endpoints)


class DriveCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(DriveCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.drive_col = drive.DriveCollection(
            self.conn, '/redfish/v1/StorageServices/NVMeoE1/Drives',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.drive_col._parse_attributes()
        self.assertEqual('1.0.2', self.drive_col.redfish_version)
        self.assertEqual('Drives',
                         self.drive_col.name)
        self.assertEqual(
            ('/redfish/v1/Chassis/1/Drives/1',
             '/redfish/v1/Chassis/1/Drives/2'),
            self.drive_col.members_identities)

    @mock.patch.object(drive, 'Drive', autospec=True)
    def test_get_member(self, mock_drive):
        self.drive_col.get_member(
            '/redfish/v1/Chassis/1/Drives/1')
        mock_drive.assert_called_once_with(
            self.drive_col._conn,
            '/redfish/v1/Chassis/1/Drives/1',
            redfish_version=self.drive_col.redfish_version)

    @mock.patch.object(drive, 'Drive', autospec=True)
    def test_get_members(self, mock_drive):
        members = self.drive_col.get_members()
        calls = [
            mock.call(self.drive_col._conn,
                      '/redfish/v1/Chassis/1/Drives/1',
                      redfish_version=self.drive_col.redfish_version),
            mock.call(self.drive_col._conn,
                      '/redfish/v1/Chassis/1/Drives/2',
                      redfish_version=self.drive_col.redfish_version)
        ]
        mock_drive.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))
