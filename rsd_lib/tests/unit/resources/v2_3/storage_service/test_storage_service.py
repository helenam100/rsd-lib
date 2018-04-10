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

from sushy import exceptions

from rsd_lib.resources.v2_3.storage_service import storage_service
from rsd_lib.resources.v2_3.storage_service import volume


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
        self.assertIsNone(self.storage_service_inst._volumes)

    def test__get_volume_collection_path(self):
        expected = '/redfish/v1/StorageServices/1/Volumes'
        result = self.storage_service_inst._get_volume_collection_path()
        self.assertEqual(expected, result)

    def test__get_volume_collection_path_missing_processors_attr(self):
        self.storage_service_inst._json.pop('Volumes')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Volumes',
            self.storage_service_inst._get_volume_collection_path)

    def test_volumes(self):
        # check for the underneath variable value
        self.assertIsNone(self.storage_service_inst._volumes)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'volume_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_volumes = self.storage_service_inst.volumes
        # | THEN |
        self.assertIsInstance(actual_volumes,
                              volume.VolumeCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_volumes,
                      self.storage_service_inst.volumes)
        self.conn.get.return_value.json.assert_not_called()

    def test_volumes_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'volume_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_service_inst.volumes,
                              volume.VolumeCollection)

        # On refreshing the storage service instance...
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_service_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.storage_service_inst._volumes)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'volume_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_service_inst.volumes,
                              volume.VolumeCollection)


class StorageServiceCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageServiceCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_service_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_service_col = storage_service.StorageServiceCollection(
            self.conn, '/redfish/v1/StorageServices', redfish_version='1.0.2')

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
