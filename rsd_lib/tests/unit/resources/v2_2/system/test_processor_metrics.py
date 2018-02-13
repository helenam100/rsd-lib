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

from rsd_lib.resources.v2_2.system import processor_metrics


class ProcessorMetricsTestCase(testtools.TestCase):

    def setUp(self):
        super(ProcessorMetricsTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'processor_metrics.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.processor_metrics_inst = processor_metrics.ProcessorMetrics(
            self.conn, '/redfish/v1/Systems/System1/Metrics',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.processor_metrics_inst._parse_attributes()
        self.assertEqual('1.1.0', self.processor_metrics_inst.redfish_version)
        self.assertEqual('ProcessorMetrics for CPU1',
                         self.processor_metrics_inst.name)
        self.assertEqual('description-as-string',
                         self.processor_metrics_inst.description)
        self.assertEqual('Metrics for CPU1',
                         self.processor_metrics_inst.identity)
        self.assertEqual(
            3014, self.processor_metrics_inst.average_frequency_mhz)
        self.assertEqual(19, self.processor_metrics_inst.throttling_celsius)
        self.assertEqual(73, self.processor_metrics_inst.temperature_celsius)
        self.assertEqual(153, self.processor_metrics_inst.consumed_power_watt)
        self.assertEqual(["FRB1 BIST Failure", "Processor Throttled"],
                         self.processor_metrics_inst.health)
