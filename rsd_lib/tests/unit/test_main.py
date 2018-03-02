# Copyright 2017 Red Hat, Inc.
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
from sushy import connector
import testtools

from rsd_lib import main
from rsd_lib.resources import v2_1
from rsd_lib.resources import v2_2


class RSDLibTestCase(testtools.TestCase):

    @mock.patch.object(connector, 'Connector', autospec=True)
    def setUp(self, mock_connector):
        super(RSDLibTestCase, self).setUp()
        self.conn = mock.Mock()
        mock_connector.return_value = self.conn
        with open('rsd_lib/tests/unit/json_samples/v2_1/root.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.rsd = main.RSDLib('http://foo.bar:8442', username='foo',
                               password='bar', verify=True)

    def test__parse_attributes(self):
        self.rsd._parse_attributes()
        self.assertEqual("2.1.0", self.rsd._rsd_api_version)
        self.assertEqual("1.0.2", self.rsd._redfish_version)

    @mock.patch.object(v2_2, 'RSDLibV2_2', autospec=True)
    @mock.patch.object(v2_1, 'RSDLibV2_1', autospec=True)
    def test_factory(self, mock_rsdlibv2_1, mock_rsdlibv2_2):
        self.rsd.factory()
        mock_rsdlibv2_1.assert_called_once_with(
            self.rsd._conn,
            self.rsd._root_prefix,
            redfish_version=self.rsd._redfish_version)

        self.rsd._rsd_api_version = "2.2.0"
        self.rsd.factory()
        mock_rsdlibv2_1.assert_called_once_with(
            self.rsd._conn,
            self.rsd._root_prefix,
            redfish_version=self.rsd._redfish_version)

    def test_factory_unsupported_version(self):
        self.rsd._rsd_api_version = "10.0.0"
        expected_error_message = "The rsd-lib library doesn't support RSD "\
                                 "API version 10.0.0."

        with self.assertRaisesRegex(NotImplementedError,
                                    expected_error_message):
            self.rsd.factory()
