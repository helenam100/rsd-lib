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

from rsd_lib.resources.v2_3.storage_service import storage_pool
from rsd_lib.resources.v2_3.storage_service import volume


class StoragePoolTestCase(testtools.TestCase):

    def setUp(self):
        super(StoragePoolTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/storage_pool.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.storage_pool_inst = storage_pool.StoragePool(
            self.conn, '/redfish/v1/StorageServices/NVMeoE1/StoragePool/2',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.storage_pool_inst._parse_attributes()
        self.assertEqual('1.0.2', self.storage_pool_inst.redfish_version)
        self.assertEqual('Base storage pool',
                         self.storage_pool_inst.description)
        self.assertEqual('2', self.storage_pool_inst.identity)
        self.assertEqual('BasePool', self.storage_pool_inst.name)
        self.assertEqual('Enabled', self.storage_pool_inst.status.state)
        self.assertEqual('OK', self.storage_pool_inst.status.health)
        self.assertEqual('OK', self.storage_pool_inst.status.health_rollup)
        self.assertEqual(512174850048,
                         self.storage_pool_inst.capacity.allocated_bytes)
        self.assertEqual(3071983104,
                         self.storage_pool_inst.capacity.consumed_bytes)
        self.assertEqual(None,
                         self.storage_pool_inst.capacity.guaranteed_bytes)
        self.assertEqual(None,
                         self.storage_pool_inst.capacity.provisioned_bytes)
        self.assertEqual(
            ('/redfish/v1/Chassis/1/Drives/2',),
            self.storage_pool_inst.capacity_sources[0].providing_drives)
        self.assertEqual(
            512174850048,
            self.storage_pool_inst.capacity_sources[0].
            provided_capacity.allocated_bytes)
        self.assertEqual(
            3071983104,
            self.storage_pool_inst.capacity_sources[0].
            provided_capacity.consumed_bytes)
        self.assertEqual(
            None,
            self.storage_pool_inst.capacity_sources[0].
            provided_capacity.guaranteed_bytes)
        self.assertEqual(
            None,
            self.storage_pool_inst.capacity_sources[0].
            provided_capacity.provisioned_bytes)

    def test__get_allocated_volumes_path(self):
        expected = '/redfish/v1/StorageServices/NVMeoE1/StoragePools/'\
                   '2/AllocatedVolumes'
        result = self.storage_pool_inst._get_allocated_volumes_path()
        self.assertEqual(expected, result)

    def test__get_allocated_volumes_path_missing_processors_attr(self):
        self.storage_pool_inst._json.pop('AllocatedVolumes')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute AllocatedVolumes',
            self.storage_pool_inst._get_allocated_volumes_path)

    def test_allocated_volumes(self):
        # check for the underneath variable value
        self.assertIsNone(self.storage_pool_inst._allocated_volumes)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'volume_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_volumes = self.storage_pool_inst.allocated_volumes
        # | THEN |
        self.assertIsInstance(actual_volumes,
                              volume.VolumeCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_volumes,
                      self.storage_pool_inst.allocated_volumes)
        self.conn.get.return_value.json.assert_not_called()

    def test_allocated_volumes_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'volume_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_pool_inst.allocated_volumes,
                              volume.VolumeCollection)

        # On refreshing the storage service instance...
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_pool.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_pool_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.storage_pool_inst._allocated_volumes)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'volume_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_pool_inst.allocated_volumes,
                              volume.VolumeCollection)

    def test__get_allocated_pools_path(self):
        expected = '/redfish/v1/StorageServices/NVMeoE1/StoragePools/'\
                   '2/AllocatedPools'
        result = self.storage_pool_inst._get_allocated_pools_path()
        self.assertEqual(expected, result)

    def test__get_allocated_pools_path_missing_processors_attr(self):
        self.storage_pool_inst._json.pop('AllocatedPools')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute AllocatedPools',
            self.storage_pool_inst._get_allocated_pools_path)

    def test_allocated_pools(self):
        # check for the underneath variable value
        self.assertIsNone(self.storage_pool_inst._allocated_pools)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_pool_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_storage_pools = self.storage_pool_inst.allocated_pools
        # | THEN |
        self.assertIsInstance(actual_storage_pools,
                              storage_pool.StoragePoolCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_storage_pools,
                      self.storage_pool_inst.allocated_pools)
        self.conn.get.return_value.json.assert_not_called()

    def test_allocated_pools_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_pool_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_pool_inst.allocated_pools,
                              storage_pool.StoragePoolCollection)

        # On refreshing the storage service instance...
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_pool.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.storage_pool_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.storage_pool_inst._allocated_pools)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_pool_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.storage_pool_inst.allocated_pools,
                              storage_pool.StoragePoolCollection)


class StoragePoolCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(StoragePoolCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_pool_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.storage_pool_col = storage_pool.StoragePoolCollection(
            self.conn, '/redfish/v1/StorageServices/NVMeoE1/StoragePools',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.storage_pool_col._parse_attributes()
        self.assertEqual('1.0.2', self.storage_pool_col.redfish_version)
        self.assertEqual('StoragePools Collection',
                         self.storage_pool_col.name)
        self.assertEqual(
            ('/redfish/v1/StorageServices/NVMeoE1/StoragePools/1',
             '/redfish/v1/StorageServices/NVMeoE1/StoragePools/2'),
            self.storage_pool_col.members_identities)

    @mock.patch.object(storage_pool, 'StoragePool', autospec=True)
    def test_get_member(self, mock_storage_pool):
        self.storage_pool_col.get_member(
            '/redfish/v1/StorageServices/NVMeoE1/StoragePools/1')
        mock_storage_pool.assert_called_once_with(
            self.storage_pool_col._conn,
            '/redfish/v1/StorageServices/NVMeoE1/StoragePools/1',
            redfish_version=self.storage_pool_col.redfish_version)

    @mock.patch.object(storage_pool, 'StoragePool', autospec=True)
    def test_get_members(self, mock_storage_pool):
        members = self.storage_pool_col.get_members()
        calls = [
            mock.call(self.storage_pool_col._conn,
                      '/redfish/v1/StorageServices/NVMeoE1/StoragePools/1',
                      redfish_version=self.storage_pool_col.redfish_version),
            mock.call(self.storage_pool_col._conn,
                      '/redfish/v1/StorageServices/NVMeoE1/StoragePools/2',
                      redfish_version=self.storage_pool_col.redfish_version)
        ]
        mock_storage_pool.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))
