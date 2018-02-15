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

from rsd_lib.resources.v2_2.telemetry.metric_definitions import cpu_health


class CPUHealthTestCase(testtools.TestCase):

    def setUp(self):
        super(CPUHealthTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'cpu_health_metric_def.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.cpu_health_metric_def_inst = cpu_health.CPUHealth(
            self.conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUHealth',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.cpu_health_metric_def_inst._parse_attributes()
        self.assertEqual('1.1.0',
                         self.cpu_health_metric_def_inst.redfish_version)
        self.assertEqual('CPU1 IPMI Health Sensor',
                         self.cpu_health_metric_def_inst.name)
        self.assertEqual('CPUHealth1',
                         self.cpu_health_metric_def_inst.identity)
        self.assertEqual('Discrete',
                         self.cpu_health_metric_def_inst.metric_type)
        self.assertEqual('PhysicalSensor',
                         self.cpu_health_metric_def_inst.sensor_type)
        self.assertEqual('PhysicalSensor',
                         self.cpu_health_metric_def_inst.implementation)
        self.assertEqual('PT1S',
                         self.cpu_health_metric_def_inst.sensing_interval)
        self.assertEqual('CPU',
                         self.cpu_health_metric_def_inst.physical_context)

        expected = [
            "OK",
            "Internal Error",
            "Thermal Trip",
            "FRB1 BIST Failure",
            "FRB2 Hang in Post",
            "FRB3 Startup Failure",
            "Config Error",
            "SMBIOS Uncorrectable Error",
            "Processor Presence Detected",
            "Processor Disabled",
            "Terminator Presence Detected",
            "Processor Throttled",
            "Machine Check Exception",
            "Correctable Machine Check Error"
        ]
        self.assertEqual(expected,
                         self.cpu_health_metric_def_inst.discrete_values)
