# Copyright 2017 Intel, Inc.
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

import copy
import mock

from sushy.resources import base as resource_base
from sushy.tests.unit import base

from rsd_lib.resources import base as rsd_resource_base

TEST_JSON = {
    'String': 'a string',
    'Integer': '42',
    'List': ['a string', 42],
    'Nested': {
        'String': 'another string',
        'Integer': 0,
        'Object': {
            'Field': 'field value'
        },
        'Mapped': 'raw'
    },
    'FieldList': [
        {
            'String': 'a third string',
            'Integer': 1
        },
        {
            'String': 'a fourth string',
            'Integer': 2
        }
    ]
}


MAPPING = {
    'raw': 'real'
}


class NestedTestField(resource_base.CompositeField):
    string = resource_base.Field('String', required=True)
    integer = resource_base.Field('Integer', adapter=int)
    nested_field = resource_base.Field(['Object', 'Field'], required=True)
    mapped = resource_base.MappedField('Mapped', MAPPING)
    non_existing = resource_base.Field('NonExisting', default=3.14)


class TestFieldList(rsd_resource_base.FieldList):
    string = resource_base.Field('String')
    integer = resource_base.Field('Integer')


class ComplexResource(resource_base.ResourceBase):
    string = resource_base.Field('String', required=True)
    integer = resource_base.Field('Integer', adapter=int)
    nested = NestedTestField('Nested')
    field_list = TestFieldList('FieldList')
    non_existing_nested = NestedTestField('NonExistingNested')
    non_existing_mapped = resource_base.MappedField('NonExistingMapped',
                                                    MAPPING)


class FieldTestCase(base.TestCase):
    def setUp(self):
        super(FieldTestCase, self).setUp()
        self.conn = mock.Mock()
        self.json = copy.deepcopy(TEST_JSON)
        self.conn.get.return_value.json.return_value = self.json
        self.test_resource = ComplexResource(self.conn,
                                             redfish_version='1.0.x')

    def test_ok(self):
        self.assertEqual('a string', self.test_resource.string)
        self.assertEqual(42, self.test_resource.integer)
        self.assertEqual('another string', self.test_resource.nested.string)
        self.assertEqual(0, self.test_resource.nested.integer)
        self.assertEqual('field value', self.test_resource.nested.nested_field)
        self.assertEqual('real', self.test_resource.nested.mapped)
        self.assertEqual(3.14, self.test_resource.nested.non_existing)
        self.assertEqual('a third string',
                         self.test_resource.field_list[0].string)
        self.assertEqual(2, self.test_resource.field_list[1].integer)
        self.assertIsNone(self.test_resource.non_existing_nested)
        self.assertIsNone(self.test_resource.non_existing_mapped)
