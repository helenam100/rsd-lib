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

from rsd_lib.resources.v2_2.system import metrics


class MetricsTestCase(testtools.TestCase):

    def setUp(self):
        super(MetricsTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/system_metrics.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.system_metrics_inst = metrics.Metrics(
            self.conn, '/redfish/v1/Systems/System1/Metrics',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.system_metrics_inst._parse_attributes()
        self.assertEqual('1.0.2', self.system_metrics_inst.redfish_version)
        self.assertEqual('Computer System Metrics for System1',
                         self.system_metrics_inst.name)
        self.assertEqual('description-as-string',
                         self.system_metrics_inst.description)
        self.assertEqual('Metrics for System1',
                         self.system_metrics_inst.identity)
        self.assertEqual(
            17, self.system_metrics_inst.processor_bandwidth_percent)
        self.assertEqual(23, self.system_metrics_inst.memory_bandwidth_percent)
        self.assertEqual(
            13, self.system_metrics_inst.memory_throttled_cycles_percent)
        self.assertEqual(120, self.system_metrics_inst.processor_power_watt)
        self.assertEqual(48, self.system_metrics_inst.memory_power_watt)
        self.assertEqual(4, self.system_metrics_inst.io_bandwidth_gbps)
        self.assertEqual(["OK"], self.system_metrics_inst.health)
