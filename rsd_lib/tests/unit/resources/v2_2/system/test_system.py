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
from sushy.resources.system import system as sushy_system

from rsd_lib.resources.v2_1.system import system as v2_1_system
from rsd_lib.resources.v2_2.system import memory
from rsd_lib.resources.v2_2.system import metrics
from rsd_lib.resources.v2_2.system import processor
from rsd_lib.resources.v2_2.system import system


class SystemTestCase(testtools.TestCase):

    def setUp(self):
        super(SystemTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/system.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.system_inst = system.System(
            self.conn, '/redfish/v1/Systems/System2',
            redfish_version='1.0.2')

    def test_class_inherit(self):
        self.assertIsInstance(self.system_inst, system.System)
        self.assertIsInstance(self.system_inst, v2_1_system.System)
        self.assertIsInstance(self.system_inst, sushy_system.System)

    def test__get_metrics_path(self):
        self.assertEqual('/redfish/v1/Systems/System2/Metrics',
                         self.system_inst._get_metrics_path())

    def test__get_metrics_path_missing_systems_attr(self):
        self.system_inst._json.get('Oem').get('Intel_RackScale').pop('Metrics')
        with self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Metrics'):
            self.system_inst._get_metrics_path()

    def test_metrics(self):
        # check for the underneath variable value
        self.assertIsNone(self.system_inst._metrics)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/system_metrics.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_metrics = self.system_inst.metrics
        # | THEN |
        self.assertIsInstance(actual_metrics,
                              metrics.Metrics)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_metrics,
                      self.system_inst.metrics)
        self.conn.get.return_value.json.assert_not_called()

    def test_metrics_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/system_metrics.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.system_inst.metrics,
                              metrics.Metrics)

        # On refreshing the system instance...
        with open('rsd_lib/tests/unit/json_samples/v2_2/system.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.system_inst.refresh()
        # | WHEN & THEN |
        self.assertIsNone(self.system_inst._metrics)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/system_metrics.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.system_inst.metrics,
                              metrics.Metrics)

    def test_processors(self):
        # check for the underneath variable value
        self.assertIsNone(self.system_inst._processors)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'processor_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_processors = self.system_inst.processors
        # | THEN |
        self.assertIsInstance(actual_processors,
                              processor.ProcessorCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_processors,
                      self.system_inst.processors)
        self.conn.get.return_value.json.assert_not_called()

    def test_processors_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'processor_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.system_inst.processors,
                              processor.ProcessorCollection)

        # On refreshing the system instance...
        with open('rsd_lib/tests/unit/json_samples/v2_2/system.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.system_inst.refresh()
        # | WHEN & THEN |
        self.assertIsNone(self.system_inst._processors)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'processor_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.system_inst.processors,
                              processor.ProcessorCollection)

    def test_memory(self):
        # check for the underneath variable value
        self.assertIsNone(self.system_inst._memory)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'memory_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_memory_col = self.system_inst.memory
        # | THEN |
        self.assertIsInstance(actual_memory_col,
                              memory.MemoryCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_memory_col,
                      self.system_inst.memory)
        self.conn.get.return_value.json.assert_not_called()

    def test_memory_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'memory_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.system_inst.memory,
                              memory.MemoryCollection)

        # On refreshing the system instance...
        with open('rsd_lib/tests/unit/json_samples/v2_2/system.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.system_inst.refresh()
        # | WHEN & THEN |
        self.assertIsNone(self.system_inst._memory)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'memory_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.system_inst.memory,
                              memory.MemoryCollection)


class SystemCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(SystemCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'system_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.system_col = system.SystemCollection(
            self.conn, '/redfish/v1/Systems',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.system_col._parse_attributes()
        self.assertEqual('1.1.0', self.system_col.redfish_version)
        self.assertEqual(('/redfish/v1/Systems/System1',
                          '/redfish/v1/Systems/System2'),
                         self.system_col.members_identities)

    @mock.patch.object(system, 'System', autospec=True)
    def test_get_member(self, mock_system):
        self.system_col.get_member(
            '/redfish/v1/Systems/System1')
        mock_system.assert_called_once_with(
            self.system_col._conn,
            '/redfish/v1/Systems/System1',
            redfish_version=self.system_col.redfish_version)

    @mock.patch.object(system, 'System', autospec=True)
    def test_get_members(self, mock_system):
        members = self.system_col.get_members()
        calls = [
            mock.call(self.system_col._conn,
                      '/redfish/v1/Systems/System1',
                      redfish_version=self.system_col.redfish_version),
            mock.call(self.system_col._conn,
                      '/redfish/v1/Systems/System2',
                      redfish_version=self.system_col.redfish_version)
        ]
        mock_system.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(2, len(members))
