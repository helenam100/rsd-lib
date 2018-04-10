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

from rsd_lib.resources.v2_3.storage_service import volume


class StorageServiceTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageServiceTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/volume.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.volume_inst = volume.Volume(
            self.conn, '/redfish/v1/StorageServices/NVMeoE1/Volumes/1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.volume_inst._parse_attributes()
        self.assertEqual('1.0.2', self.volume_inst.redfish_version)
        self.assertEqual('Volume description', self.volume_inst.description)
        self.assertEqual('1', self.volume_inst.identity)
        self.assertEqual('NVMe remote storage', self.volume_inst.name)
        self.assertEqual('Enabled', self.volume_inst.status.state)
        self.assertEqual('OK', self.volume_inst.status.health)
        self.assertEqual('OK', self.volume_inst.status.health_rollup)
        self.assertEqual(None, self.volume_inst.model)
        self.assertEqual(None, self.volume_inst.manufacturer)
        self.assertEqual(['Read', 'Write'],
                         self.volume_inst.access_capabilities)
        self.assertEqual(3071983104, self.volume_inst.capacity_bytes)
        self.assertEqual(3071983104, self.volume_inst.allocated_Bytes)
        self.assertEqual(('/redfish/v1/StorageServices/1/StoragePools/2',),
                         self.volume_inst.capacity_sources[0].providing_pools)
        self.assertEqual(3071983104,
                         self.volume_inst.capacity_sources[0].allocated_Bytes)
        self.assertEqual(('/redfish/v1/Fabrics/NVMeoE/Endpoints/1',),
                         self.volume_inst.links.endpoints)
        self.assertEqual(
            '/redfish/v1/StorageServices/NVMeoE1/Volumes/1/Metrics',
            self.volume_inst.links.metrics)
        self.assertEqual(
            'SourceElement',
            self.volume_inst.replica_infos[0].replica_readonly_access)
        self.assertEqual('Snapshot',
                         self.volume_inst.replica_infos[0].replica_type)
        self.assertEqual('Target',
                         self.volume_inst.replica_infos[0].replica_role)
        self.assertEqual('/redfish/v1/StorageServices/NVMeoE1/Volumes/2',
                         self.volume_inst.replica_infos[0].replica)
        self.assertEqual(False, self.volume_inst.bootable)
        self.assertEqual(None, self.volume_inst.erased)
        self.assertEqual(True, self.volume_inst.erase_on_detach)
