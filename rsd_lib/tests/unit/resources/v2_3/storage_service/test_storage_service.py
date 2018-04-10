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

from rsd_lib.resources.v2_3.storage_service import storage_service


class StorageServiceTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageServiceTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/storage_service.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.storage_service_inst = storage_service.StorageService(
            self.conn, '/redfish/v1/StorageServices/NVMeoE1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.storage_service_inst._parse_attributes()
        self.assertEqual('1.0.2', self.storage_service_inst.redfish_version)
        self.assertEqual('Storage Service description',
                         self.storage_service_inst.description)
        self.assertEqual('NVMeoE1', self.storage_service_inst.identity)
        self.assertEqual('Storage Service', self.storage_service_inst.name)
        self.assertEqual('Enabled', self.storage_service_inst.status.state)
        self.assertEqual('OK', self.storage_service_inst.status.health)
        self.assertEqual('OK', self.storage_service_inst.status.health_rollup)


class StorageServiceCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageServiceCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_service_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_service_col = storage_service.StorageServiceCollection(
            self.conn, '/redfish/v1/Services', redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.storage_service_col._parse_attributes()
        self.assertEqual('1.0.2', self.storage_service_col.redfish_version)
        self.assertEqual('Storage Services Collection',
                         self.storage_service_col.name)
        self.assertEqual(('/redfish/v1/StorageServices/NVMeoE1',),
                         self.storage_service_col.members_identities)

    @mock.patch.object(storage_service, 'StorageService', autospec=True)
    def test_get_member(self, mock_storage_service):
        self.storage_service_col.get_member(
            '/redfish/v1/StorageServices/NVMeoE1')
        mock_storage_service.assert_called_once_with(
            self.storage_service_col._conn,
            '/redfish/v1/StorageServices/NVMeoE1',
            redfish_version=self.storage_service_col.redfish_version)

    @mock.patch.object(storage_service, 'StorageService', autospec=True)
    def test_get_members(self, mock_storage_service):
        members = self.storage_service_col.get_members()
        mock_storage_service.assert_called_once_with(
            self.storage_service_col._conn,
            '/redfish/v1/StorageServices/NVMeoE1',
            redfish_version=self.storage_service_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
