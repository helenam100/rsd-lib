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

from rsd_lib.resources.v2_2.telemetry.metric_definitions import cpu_bandwidth
from rsd_lib.resources.v2_2.telemetry.metric_definitions import cpu_health
from rsd_lib.resources.v2_2.telemetry.metric_definitions import cpu_temperature
from rsd_lib.resources.v2_2.telemetry.metric_definitions \
    import metric_definitions


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

    @mock.patch.object(cpu_bandwidth, 'CPUBandwidth', autospec=True)
    @mock.patch.object(cpu_health, 'CPUHealth', autospec=True)
    @mock.patch.object(cpu_temperature, 'CPUTemperature', autospec=True)
    def test_get_member(self, mock_cpu_temperature, mock_cpu_health,
                        mock_cpu_bandwidth):
        self.metric_def_col.get_member(
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUTemperature')
        mock_cpu_temperature.assert_called_once_with(
            self.metric_def_col._conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUTemperature',
            redfish_version=self.metric_def_col.redfish_version)

        self.metric_def_col.get_member(
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUHealth')
        mock_cpu_health.assert_called_once_with(
            self.metric_def_col._conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUHealth',
            redfish_version=self.metric_def_col.redfish_version)

        self.metric_def_col.get_member(
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUBandwidth')
        mock_cpu_bandwidth.assert_called_once_with(
            self.metric_def_col._conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUBandwidth',
            redfish_version=self.metric_def_col.redfish_version)

    @mock.patch.object(cpu_bandwidth, 'CPUBandwidth', autospec=True)
    @mock.patch.object(cpu_health, 'CPUHealth', autospec=True)
    @mock.patch.object(cpu_temperature, 'CPUTemperature', autospec=True)
    def test_get_members(self, mock_cpu_temperature, mock_cpu_health,
                         mock_cpu_bandwidth):
        members = self.metric_def_col.get_members()

        mock_cpu_temperature.assert_called_once_with(
            self.metric_def_col._conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUTemperature',
            redfish_version=self.metric_def_col.redfish_version)
        mock_cpu_health.assert_called_once_with(
            self.metric_def_col._conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUHealth',
            redfish_version=self.metric_def_col.redfish_version)
        mock_cpu_bandwidth.assert_called_once_with(
            self.metric_def_col._conn,
            '/redfish/v1/TelemetryService/MetricDefinitions/CPUBandwidth',
            redfish_version=self.metric_def_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(3, len(members))
