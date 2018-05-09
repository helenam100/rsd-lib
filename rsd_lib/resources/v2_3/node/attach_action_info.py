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

import logging

from sushy.resources import base
from sushy import utils

LOG = logging.getLogger(__name__)

NAME_MAPPING = {
    "Name": "name",
    "Required": "required",
    "DataType": "data_type",
    "ObjectDataType": "object_data_type",
    "AllowableValues": "allowable_values"
}


class AttachResourceActionInfo(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The storage pool  identity string"""

    description = base.Field('Description')
    """The storage pool  description string"""

    name = base.Field('Name')
    """The storage pool  name string"""

    _parameters = None  # ref to allocated volumes collection

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a LogicalDrive

        :param connector: A Connector instance
        :param identity: The identity of the AttachResourceActionInfo resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(AttachResourceActionInfo, self).__init__(
            connector, identity, redfish_version)

    @property
    def parameters(self):
        """Property to provide reference to `Parameters` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        if self._parameters is None:
            self._parameters = []
            for i in self.json.get('Parameters'):
                item = {}
                for key in NAME_MAPPING:
                    item[NAME_MAPPING[key]] = i[key]

                if item['name'] == 'Resource':
                    item['allowable_values'] = utils.get_members_identities(
                        item['allowable_values'])

                self._parameters.append(item)

        return self._parameters

    def refresh(self):
        super(AttachResourceActionInfo, self).refresh()
        self._parameters = None
