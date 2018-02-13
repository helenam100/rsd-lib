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

from rsd_lib.resources.v2_2.system import processor
from rsd_lib.resources.v2_2.system import processor_metrics


class ProcessorTestCase(testtools.TestCase):

    def setUp(self):
        super(ProcessorTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/processor.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.processor_inst = processor.Processor(
            self.conn, '/redfish/v1/Systems/System1/Processors/CPU1',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.processor_inst._parse_attributes()
        self.assertEqual('1.1.0', self.processor_inst.redfish_version)
        self.assertEqual('CPU1', self.processor_inst.identity)
        self.assertEqual('CPU 1', self.processor_inst.socket)
        self.assertEqual('CPU', self.processor_inst.processor_type)
        self.assertEqual('x86 or x86-64',
                         self.processor_inst.processor_architecture)
        self.assertEqual('x86-64', self.processor_inst.instruction_set)
        self.assertEqual('Intel(R) Corporation',
                         self.processor_inst.manufacturer)
        self.assertEqual('Multi-Core Intel(R) Xeon(R) processor 7xxx Series',
                         self.processor_inst.model)
        self.assertEqual(3700, self.processor_inst.max_speed_mhz)
        self.assertEqual(8, self.processor_inst.total_cores)
        self.assertEqual(16, self.processor_inst.total_threads)
        self.assertEqual('Enabled', self.processor_inst.status.state)
        self.assertEqual('OK', self.processor_inst.status.health)
        self.assertEqual('OK', self.processor_inst.status.health_rollup)

    def test__get_metrics_path(self):
        self.assertEqual('/redfish/v1/Systems/System1/Processors/CPU1/Metrics',
                         self.processor_inst._get_metrics_path())

    def test__get_metrics_path_missing_systems_attr(self):
        self.processor_inst._json.get('Oem').get('Intel_RackScale')\
            .pop('Metrics')
        with self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Processor Metrics'):
            self.processor_inst._get_metrics_path()

    def test_metrics(self):
        # check for the underneath variable value
        self.assertIsNone(self.processor_inst._metrics)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'processor_metrics.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_metrics = self.processor_inst.metrics
        # | THEN |
        self.assertIsInstance(actual_metrics,
                              processor_metrics.ProcessorMetrics)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_metrics,
                      self.processor_inst.metrics)
        self.conn.get.return_value.json.assert_not_called()

    def test_metrics_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'processor_metrics.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.processor_inst.metrics,
                              processor_metrics.ProcessorMetrics)

        # On refreshing the processor instance...
        with open('rsd_lib/tests/unit/json_samples/v2_2/processor.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.processor_inst.refresh()
        # | WHEN & THEN |
        self.assertIsNone(self.processor_inst._metrics)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'processor_metrics.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.processor_inst.metrics,
                              processor_metrics.ProcessorMetrics)
