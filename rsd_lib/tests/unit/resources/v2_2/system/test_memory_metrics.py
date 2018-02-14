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

from rsd_lib.resources.v2_2.system import memory_metrics


class MemoryMetricsTestCase(testtools.TestCase):

    def setUp(self):
        super(MemoryMetricsTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'memory_metrics.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.memory_metrics_inst = memory_metrics.MemoryMetrics(
            self.conn, '/redfish/v1/Systems/3/Memory/Dimm1/Metrics',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.memory_metrics_inst._parse_attributes()
        self.assertEqual('1.1.0', self.memory_metrics_inst.redfish_version)
        self.assertEqual('Memory Metrics for DIMM1',
                         self.memory_metrics_inst.name)
        self.assertEqual('description-as-string',
                         self.memory_metrics_inst.description)
        self.assertEqual('Metrics for DIMM1',
                         self.memory_metrics_inst.identity)
        self.assertEqual(46, self.memory_metrics_inst.temperature_celsius)
        self.assertEqual(["OK"], self.memory_metrics_inst.health)
