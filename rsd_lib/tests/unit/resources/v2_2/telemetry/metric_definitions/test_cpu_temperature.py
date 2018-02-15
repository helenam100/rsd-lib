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

from rsd_lib.resources.v2_2.telemetry.metric_definitions import cpu_temperature


class CPUTemperatureTestCase(testtools.TestCase):

    def setUp(self):
        super(CPUTemperatureTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'cpu_temperature_metric_def.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.cpu_temperature_metric_def_inst = cpu_temperature.CPUTemperature(
            self.conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUTemperature',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.cpu_temperature_metric_def_inst._parse_attributes()
        self.assertEqual('1.1.0',
                         self.cpu_temperature_metric_def_inst.redfish_version)
        self.assertEqual('Temperature MetricDefinition',
                         self.cpu_temperature_metric_def_inst.name)
        self.assertEqual('TEMP1',
                         self.cpu_temperature_metric_def_inst.identity)
        self.assertEqual('Numeric',
                         self.cpu_temperature_metric_def_inst.metric_type)
        self.assertEqual('Temperature',
                         self.cpu_temperature_metric_def_inst.sensor_type)
        self.assertEqual('Physical',
                         self.cpu_temperature_metric_def_inst.implementation)
        self.assertEqual('PT1S',
                         self.cpu_temperature_metric_def_inst.sensing_interval)
        self.assertEqual('CPU',
                         self.cpu_temperature_metric_def_inst.physical_context)
        self.assertEqual('Cel', self.cpu_temperature_metric_def_inst.units)
        self.assertEqual(
            0, self.cpu_temperature_metric_def_inst.min_reading_range)
        self.assertEqual(
            80, self.cpu_temperature_metric_def_inst.max_reading_range)
        self.assertEqual(1, self.cpu_temperature_metric_def_inst.precision)
        self.assertEqual(2, self.cpu_temperature_metric_def_inst.calibration)
