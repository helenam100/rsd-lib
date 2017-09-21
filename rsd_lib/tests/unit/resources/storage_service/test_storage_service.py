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

from rsd_lib.resources.storage_service import logical_drive
from rsd_lib.resources.storage_service import physical_drive
from rsd_lib.resources.storage_service import remote_target
from rsd_lib.resources.storage_service import storage_service


class StorageServiceTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageServiceTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/storage_service.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.storage_service_inst = storage_service.StorageService(
            self.conn, '/redfish/v1/Nodes/RSS1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.storage_service_inst._parse_attributes()
        self.assertEqual('1.0.2', self.storage_service_inst.redfish_version)
        self.assertEqual('Storage Service',
                         self.storage_service_inst.description)
        self.assertEqual('RSS1', self.storage_service_inst.identity)
        self.assertEqual('Storage Service', self.storage_service_inst.name)
        self.assertEqual('Enabled', self.storage_service_inst.status.state)
        self.assertEqual('OK', self.storage_service_inst.status.health)
        self.assertIsNone(self.storage_service_inst._logical_drives)
        self.assertIsNone(self.storage_service_inst._physical_drives)
        self.assertIsNone(self.storage_service_inst._remote_targets)

    def test__get_logical_drive_collection_path_missing_processors_attr(self):
        self.storage_service_inst._json.pop('LogicalDrives')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute LogicalDrives',
            self.storage_service_inst._get_logical_drive_collection_path)

    def test_logical_drives(self):
        # check for the underneath variable value
        self.assertIsNone(self.storage_service_inst._logical_drives)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'logical_drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_logical_drives = self.storage_service_inst.logical_drives
        # | THEN |
        self.assertIsInstance(actual_logical_drives,
                              logical_drive.LogicalDriveCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_logical_drives,
                      self.storage_service_inst.logical_drives)
        self.conn.get.return_value.json.assert_not_called()

    def test_logical_drives_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'logical_drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_service_inst.logical_drives,
                              logical_drive.LogicalDriveCollection)

        # On refreshing the storage service instance...
        with open('rsd_lib/tests/unit/json_samples/'
                  'storage_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_service_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.storage_service_inst._logical_drives)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'logical_drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_service_inst.logical_drives,
                              logical_drive.LogicalDriveCollection)

    def test__get_physical_drive_collection_path_missing_processors_attr(self):
        self.storage_service_inst._json.pop('Drives')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute PhysicalDrives',
            self.storage_service_inst._get_physical_drive_collection_path)

    def test_physical_drives(self):
        # check for the underneath variable value
        self.assertIsNone(self.storage_service_inst._physical_drives)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'physical_drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_physical_drives = self.storage_service_inst.physical_drives
        # | THEN |
        self.assertIsInstance(actual_physical_drives,
                              physical_drive.PhysicalDriveCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_physical_drives,
                      self.storage_service_inst.physical_drives)
        self.conn.get.return_value.json.assert_not_called()

    def test_physical_drives_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'physical_drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_service_inst.physical_drives,
                              physical_drive.PhysicalDriveCollection)

        # On refreshing the storage service instance...
        with open('rsd_lib/tests/unit/json_samples/'
                  'storage_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_service_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.storage_service_inst._physical_drives)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'physical_drive_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_service_inst.physical_drives,
                              physical_drive.PhysicalDriveCollection)

    def test__get_remote_target_collection_path_missing_processors_attr(self):
        self.storage_service_inst._json.pop('RemoteTargets')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute RemoteTargets',
            self.storage_service_inst._get_remote_target_collection_path)

    def test_remote_targets(self):
        # check for the underneath variable value
        self.assertIsNone(self.storage_service_inst._remote_targets)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'remote_target_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_remote_targets = self.storage_service_inst.remote_targets
        # | THEN |
        self.assertIsInstance(actual_remote_targets,
                              remote_target.RemoteTargetCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_remote_targets,
                      self.storage_service_inst.remote_targets)
        self.conn.get.return_value.json.assert_not_called()

    def test_remote_targets_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'remote_target_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_service_inst.remote_targets,
                              remote_target.RemoteTargetCollection)

        # On refreshing the storage service instance...
        with open('rsd_lib/tests/unit/json_samples/'
                  'storage_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_service_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.storage_service_inst._remote_targets)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/'
                  'remote_target_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_service_inst.remote_targets,
                              remote_target.RemoteTargetCollection)


class StorageServiceCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(StorageServiceCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/'
                  'storage_service_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_service_col = storage_service.StorageServiceCollection(
            self.conn, '/redfish/v1/Services', redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.storage_service_col._parse_attributes()
        self.assertEqual('1.0.2', self.storage_service_col.redfish_version)
        self.assertEqual('Storage Services Collection',
                         self.storage_service_col.name)
        self.assertEqual(('/redfish/v1/Services/RSS1',),
                         self.storage_service_col.members_identities)

    @mock.patch.object(storage_service, 'StorageService', autospec=True)
    def test_get_member(self, mock_storage_service):
        self.storage_service_col.get_member('/redfish/v1/Services/RSS1')
        mock_storage_service.assert_called_once_with(
            self.storage_service_col._conn, '/redfish/v1/Services/RSS1',
            redfish_version=self.storage_service_col.redfish_version)

    @mock.patch.object(storage_service, 'StorageService', autospec=True)
    def test_get_members(self, mock_storage_service):
        members = self.storage_service_col.get_members()
        mock_storage_service.assert_called_once_with(
            self.storage_service_col._conn, '/redfish/v1/Services/RSS1',
            redfish_version=self.storage_service_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
