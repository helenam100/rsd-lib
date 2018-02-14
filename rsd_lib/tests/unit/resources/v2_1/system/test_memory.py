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

from rsd_lib.resources.v2_1.system import memory


class MemoryTestCase(testtools.TestCase):

    def setUp(self):
        super(MemoryTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/memory.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.memory_inst = memory.Memory(
            self.conn, '/redfish/v1/Systems/System1/Memory/Dimm1',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.memory_inst._parse_attributes()
        self.assertEqual('1.1.0', self.memory_inst.redfish_version)
        self.assertEqual('DIMM', self.memory_inst.name)
        self.assertEqual('Dimm1', self.memory_inst.identity)
        self.assertEqual('DRAM', self.memory_inst.memory_type)
        self.assertEqual('DDR4', self.memory_inst.memory_device_type)
        self.assertEqual('LRDIMM', self.memory_inst.base_module_type)
        self.assertEqual(['DRAM'], self.memory_inst.memory_media)
        self.assertEqual(16384, self.memory_inst.capacity_mib)
        self.assertEqual(64, self.memory_inst.data_width_bits)
        self.assertEqual(72, self.memory_inst.bus_width_bits)
        self.assertEqual('Contoso', self.memory_inst.manufacturer)
        self.assertEqual('1A2B3B', self.memory_inst.serial_number)
        self.assertEqual('1A2B3D', self.memory_inst.part_number)
        self.assertEqual([2133, 2400, 2667],
                         self.memory_inst.allowed_speeds_mhz)
        self.assertEqual('RevAbc', self.memory_inst.firmware_revision)
        self.assertEqual('ApiAbc', self.memory_inst.frirmware_api_version)
        self.assertEqual(['Volatile'], self.memory_inst.function_classes)
        self.assertEqual('vendorX', self.memory_inst.vendor_id)
        self.assertEqual('deviceX', self.memory_inst.device_id)
        self.assertEqual(1, self.memory_inst.rank_count)
        self.assertEqual('PROC 1 DIMM 1', self.memory_inst.device_locator)
        self.assertEqual('MultiBitECC', self.memory_inst.error_correction)
        self.assertEqual(2400, self.memory_inst.operating_speed_mhz)
        self.assertEqual(['Volatile'], self.memory_inst.operating_memory_modes)
        self.assertEqual(1, self.memory_inst.memory_location.socket)
        self.assertEqual(1, self.memory_inst.memory_location.memory_controller)
        self.assertEqual(1, self.memory_inst.memory_location.channel)
        self.assertEqual(1, self.memory_inst.memory_location.slot)
        self.assertEqual('Enabled', self.memory_inst.status.state)
        self.assertEqual('OK', self.memory_inst.status.health)
        self.assertEqual('OK', self.memory_inst.status.health_rollup)


class MemoryCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(MemoryCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_1/'
                  'memory_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_memory_col = memory.MemoryCollection(
            self.conn, '/redfish/v1/Systems/System1/Memory',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.sys_memory_col._parse_attributes()
        self.assertEqual('1.1.0', self.sys_memory_col.redfish_version)
        self.assertEqual(('/redfish/v1/Systems/System1/Memory/Dimm1',
                          '/redfish/v1/Systems/System1/Memory/Dimm2'),
                         self.sys_memory_col.members_identities)

    @mock.patch.object(memory, 'Memory', autospec=True)
    def test_get_member(self, mock_memory):
        self.sys_memory_col.get_member(
            '/redfish/v1/Systems/System1/Memory/Dimm1')
        mock_memory.assert_called_once_with(
            self.sys_memory_col._conn,
            '/redfish/v1/Systems/System1/Memory/Dimm1',
            redfish_version=self.sys_memory_col.redfish_version)

    @mock.patch.object(memory, 'Memory', autospec=True)
    def test_get_members(self, mock_memory):
        members = self.sys_memory_col.get_members()
        calls = [
            mock.call(self.sys_memory_col._conn,
                      '/redfish/v1/Systems/System1/Memory/Dimm1',
                      redfish_version=self.sys_memory_col.redfish_version),
            mock.call(self.sys_memory_col._conn,
                      '/redfish/v1/Systems/System1/Memory/Dimm2',
                      redfish_version=self.sys_memory_col.redfish_version)
        ]
        mock_memory.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))
