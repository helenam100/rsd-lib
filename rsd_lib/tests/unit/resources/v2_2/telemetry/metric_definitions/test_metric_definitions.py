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

from rsd_lib.resources.v2_2.telemetry.metric_definitions \
    import metric_definitions


class MetricDefinitionTestCase(testtools.TestCase):

    def setUp(self):
        super(MetricDefinitionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'metric_definition.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.metric_definition_inst = metric_definitions.MetricDefinition(
            self.conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/1-md-6',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.metric_definition_inst._parse_attributes()
        self.assertEqual('1.1.0',
                         self.metric_definition_inst.redfish_version)
        self.assertEqual('memoryTemperature',
                         self.metric_definition_inst.name)
        self.assertEqual('1-md-6',
                         self.metric_definition_inst.identity)
        self.assertEqual('Numeric',
                         self.metric_definition_inst.metric_type)
        self.assertEqual('Temperature',
                         self.metric_definition_inst.sensor_type)
        self.assertEqual('PhysicalSensor',
                         self.metric_definition_inst.implementation)
        self.assertEqual('10.0s',
                         self.metric_definition_inst.sensing_interval)
        self.assertEqual('SystemBoard',
                         self.metric_definition_inst.physical_context)
        self.assertEqual('Celsius',
                         self.metric_definition_inst.units)
        self.assertEqual(
            None, self.metric_definition_inst.min_reading_range)
        self.assertEqual(
            None, self.metric_definition_inst.max_reading_range)
        self.assertEqual([], self.metric_definition_inst.discrete_values)
        self.assertEqual(
            None, self.metric_definition_inst.precision)
        self.assertEqual(
            None, self.metric_definition_inst.calibration)
        self.assertEqual(
            True, self.metric_definition_inst.isLinear)
        self.assertEqual(
            False, self.metric_definition_inst.calculable)
        self.assertEqual(
            None, self.metric_definition_inst.data_type)
        self.assertEqual(
            None, self.metric_definition_inst.accuracy)
        self.assertEqual(
            None, self.metric_definition_inst.time_stamp_accuracy)
        self.assertEqual(
            None, self.metric_definition_inst.calculation_time_interval)
        self.assertEqual(
            None, self.metric_definition_inst.calculation_algorithm)
        self.assertEqual(
            [], self.metric_definition_inst.calculation_parameters)
        self.assertEqual(
            [], self.metric_definition_inst.wildcards)

        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'cpu_bandwidth_metric_def.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.metric_definition_inst.refresh()
        self.assertEqual('1.1.0',
                         self.metric_definition_inst.redfish_version)
        self.assertEqual('CPU Bandwidth type',
                         self.metric_definition_inst.name)
        self.assertEqual('CPUBandwidth',
                         self.metric_definition_inst.identity)
        self.assertEqual('Numeric',
                         self.metric_definition_inst.metric_type)
        self.assertEqual('DigitalMeter',
                         self.metric_definition_inst.implementation)
        self.assertEqual('PT1S',
                         self.metric_definition_inst.sensing_interval)
        self.assertEqual('CPU',
                         self.metric_definition_inst.physical_context)
        self.assertEqual('%', self.metric_definition_inst.units)
        self.assertEqual(
            0, self.metric_definition_inst.min_reading_range)
        self.assertEqual(
            100, self.metric_definition_inst.max_reading_range)

        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'cpu_health_metric_def.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.metric_definition_inst.refresh()
        self.assertEqual('1.1.0',
                         self.metric_definition_inst.redfish_version)
        self.assertEqual('CPU1 IPMI Health Sensor',
                         self.metric_definition_inst.name)
        self.assertEqual('CPUHealth1',
                         self.metric_definition_inst.identity)
        self.assertEqual('Discrete',
                         self.metric_definition_inst.metric_type)
        self.assertEqual('PhysicalSensor',
                         self.metric_definition_inst.sensor_type)
        self.assertEqual('PhysicalSensor',
                         self.metric_definition_inst.implementation)
        self.assertEqual('PT1S',
                         self.metric_definition_inst.sensing_interval)
        self.assertEqual('CPU',
                         self.metric_definition_inst.physical_context)

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
                         self.metric_definition_inst.discrete_values)

        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'cpu_temperature_metric_def.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.metric_definition_inst.refresh()
        self.assertEqual('1.1.0',
                         self.metric_definition_inst.redfish_version)
        self.assertEqual('Temperature MetricDefinition',
                         self.metric_definition_inst.name)
        self.assertEqual('TEMP1',
                         self.metric_definition_inst.identity)
        self.assertEqual('Numeric',
                         self.metric_definition_inst.metric_type)
        self.assertEqual('Temperature',
                         self.metric_definition_inst.sensor_type)
        self.assertEqual('Physical',
                         self.metric_definition_inst.implementation)
        self.assertEqual('PT1S',
                         self.metric_definition_inst.sensing_interval)
        self.assertEqual('CPU',
                         self.metric_definition_inst.physical_context)
        self.assertEqual('Cel', self.metric_definition_inst.units)
        self.assertEqual(
            0, self.metric_definition_inst.min_reading_range)
        self.assertEqual(
            80, self.metric_definition_inst.max_reading_range)
        self.assertEqual(1, self.metric_definition_inst.precision)
        self.assertEqual(2, self.metric_definition_inst.calibration)


class MetricDefinitionsCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(MetricDefinitionsCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'metric_definitions.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.metric_def_col = metric_definitions.MetricDefinitionsCollection(
            self.conn, '/redfish/v1/TelemetryService/MetricDefinitions',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.metric_def_col._parse_attributes()
        self.assertEqual('1.1.0', self.metric_def_col.redfish_version)
        self.assertEqual(
            ('/redfish/v1/TelemetryService/MetricDefinitions/CPUTemperature',
             '/redfish/v1/TelemetryService/MetricDefinitions/CPUHealth',
             '/redfish/v1/TelemetryService/MetricDefinitions/CPUBandwidth'),
            self.metric_def_col.members_identities)

    @mock.patch.object(metric_definitions, 'MetricDefinition', autospec=True)
    def test_get_member(self, mock_metric_definition):
        self.metric_def_col.get_member(
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUTemperature')
        mock_metric_definition.assert_called_once_with(
            self.metric_def_col._conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUTemperature',
            redfish_version=self.metric_def_col.redfish_version)

    @mock.patch.object(metric_definitions, 'MetricDefinition', autospec=True)
    def test_get_members(self, mock_metric_definition):
        members = self.metric_def_col.get_members()

        calls = [
            mock.call(
                self.metric_def_col._conn,
                '/redfish/v1/TelemetryService/MetricDefinitions/'
                'CPUTemperature',
                redfish_version=self.metric_def_col.redfish_version),
            mock.call(
                self.metric_def_col._conn,
                '/redfish/v1/TelemetryService/MetricDefinitions/CPUHealth',
                redfish_version=self.metric_def_col.redfish_version),
            mock.call(
                self.metric_def_col._conn,
                '/redfish/v1/TelemetryService/MetricDefinitions/CPUBandwidth',
                redfish_version=self.metric_def_col.redfish_version)
        ]
        mock_metric_definition.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(3, len(members))
