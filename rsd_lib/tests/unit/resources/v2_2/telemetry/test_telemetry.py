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

from rsd_lib.resources.v2_2.telemetry.metric_definitions \
    import metric_definitions
from rsd_lib.resources.v2_2.telemetry import telemetry


class TelemetryTestCase(testtools.TestCase):

    def setUp(self):
        super(TelemetryTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'telemetry_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.telemetry_inst = telemetry.Telemetry(
            self.conn, '/redfish/v1/TelemetryService',
            redfish_version='1.1.0')

    def test__parse_attributes(self):
        self.telemetry_inst._parse_attributes()
        self.assertEqual('1.1.0', self.telemetry_inst.redfish_version)
        self.assertEqual('Enabled', self.telemetry_inst.status.state)
        self.assertEqual('OK', self.telemetry_inst.status.health)

    def test__get_metric_definitions_path(self):
        self.assertEqual('/redfish/v1/TelemetryService/MetricDefinitions',
                         self.telemetry_inst._get_metric_definitions_path())

    def test__get_metric_definitions_path_missing_systems_attr(self):
        self.telemetry_inst._json.pop('MetricDefinitions')
        with self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute MetricDefinitions'):
            self.telemetry_inst._get_metric_definitions_path()

    def test_metric_definitions(self):
        # check for the underneath variable value
        self.assertIsNone(self.telemetry_inst._metric_definitions)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'metric_definitions.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_metric_definitions = self.telemetry_inst.metric_definitions
        # | THEN |
        self.assertIsInstance(actual_metric_definitions,
                              metric_definitions.MetricDefinitionsCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_metric_definitions,
                      self.telemetry_inst.metric_definitions)
        self.conn.get.return_value.json.assert_not_called()

    def test_metrics_on_refresh(self):
        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'metric_definitions.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.telemetry_inst.metric_definitions,
                              metric_definitions.MetricDefinitionsCollection)

        # On refreshing the telemetry service instance...
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'telemetry_service.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.telemetry_inst.refresh()
        # | WHEN & THEN |
        self.assertIsNone(self.telemetry_inst._metric_definitions)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_2/'
                  'metric_definitions.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.telemetry_inst.metric_definitions,
                              metric_definitions.MetricDefinitionsCollection)
