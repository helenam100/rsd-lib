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

from sushy.resources import base


class FieldList(base.CompositeField):
    """Base class for fields consisting of a list of several sub-fields."""

    def _load(self, body, resource, nested_in=None):
        """Load the field list.

        :param body: parent JSON body.
        :param resource: parent resource.
        :param nested_in: parent resource name (for error reporting only).
        :returns: a new list object containing subfields.
        """
        nested_in = (nested_in or []) + self._path
        values = base.Field._load(self, body, resource)
        if values is None:
            return None

        # Initialize the list that will contain each field instance
        instances = []
        for value in values:
            instance = copy.copy(self)
            for attr, field in self._subfields.items():
                # Hide the Field object behind the real value
                setattr(instance, attr, field._load(value,
                                                    resource,
                                                    nested_in))
            instances.append(instance)

        return instances
