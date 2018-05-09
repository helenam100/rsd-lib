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

from rsd_lib.resources.v2_3.node import attach_action_info


class AttachResourceActionInfoTestCase(testtools.TestCase):

    def setUp(self):
        super(AttachResourceActionInfoTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'attach_action_info.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.attach_action_info = attach_action_info.AttachResourceActionInfo(
            self.conn, '/redfish/v1/Nodes/2/Actions/AttachResourceActionInfo',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.attach_action_info._parse_attributes()
        self.assertEqual('1.0.2', self.attach_action_info.redfish_version)
        self.assertEqual(None, self.attach_action_info.description)
        self.assertEqual('AttachResourceActionInfo',
                         self.attach_action_info.identity)
        self.assertEqual('Attach Resource ActionInfo',
                         self.attach_action_info.name)
        self.assertIsNone(self.attach_action_info._parameters)

    def test_parameters(self):
        # check for the underneath variable value
        self.assertIsNone(self.attach_action_info._parameters)

        # | WHEN |
        actual_parameters = self.attach_action_info.parameters
        # | THEN |
        expected = [
            {
                "name": "Resource",
                "required": True,
                "data_type": "Object",
                "object_data_type": "#Resource.Resource",
                "allowable_values": (
                    "/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1",
                )
            },
            {
                "name": "Protocol",
                "required": False,
                "data_type": "String",
                "object_data_type": None,
                "allowable_values": ["NVMeOverFabrics"]
            }
        ]
        self.assertEqual(expected, actual_parameters)

        # tests for same object on invoking subsequently
        self.assertIs(actual_parameters,
                      self.attach_action_info.parameters)

    def test_parameters_on_refresh(self):
        expected = [
            {
                "name": "Resource",
                "required": True,
                "data_type": "Object",
                "object_data_type": "#Resource.Resource",
                "allowable_values": (
                    "/redfish/v1/StorageServices/1-sv-1/Volumes/1-sv-1-vl-1",
                )
            },
            {
                "name": "Protocol",
                "required": False,
                "data_type": "String",
                "object_data_type": None,
                "allowable_values": ["NVMeOverFabrics"]
            }
        ]
        self.assertEqual(expected, self.attach_action_info.parameters)

        # On refreshing the storage service instance...
        self.attach_action_info.refresh()
        # | WHEN & THEN |
        self.assertIsNone(self.attach_action_info._parameters)

        # | GIVEN |
        with open('rsd_lib/tests/unit/json_samples/v2_3/'
                  'storage_pool_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertEqual(expected, self.attach_action_info.parameters)
