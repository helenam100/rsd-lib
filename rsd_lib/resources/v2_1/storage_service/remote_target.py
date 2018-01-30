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

import logging

from sushy.resources import base

from rsd_lib.resources import base as rsd_base

LOG = logging.getLogger(__name__)


class TargetLunField(rsd_base.FieldList):
    lun = base.Field('LUN')


class ISCSIAddressField(base.CompositeField):
    target_lun = TargetLunField('TargetLUN')
    target_iqn = base.Field('TargetIQN')
    target_portal_ip = base.Field('TargetPortalIP')
    target_portal_port = base.Field('TargetPortalPort')


class AddressesField(rsd_base.FieldList):
    iscsi = ISCSIAddressField('iSCSI')


class ISCSIInitiatorField(base.CompositeField):
    iqn = base.Field('InitiatorIQN')


class InitiatorsField(rsd_base.FieldList):
    iscsi = ISCSIInitiatorField('iSCSI')


class RemoteTarget(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The target identity string"""

    target_type = base.Field('Type')
    """Type of target"""

    addresses = AddressesField('Addresses')

    initiators = InitiatorsField('Initiator')

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a RemoteTarget

        :param connector: A Connector instance
        :param identity: The identity of the RemoteTarget resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(RemoteTarget, self).__init__(connector, identity,
                                           redfish_version)


class RemoteTargetCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return RemoteTarget

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a RemoteTargetCollection

        :param connector: A Connector instance
        :param path: The canonical path to the RemoteTarget collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(RemoteTargetCollection, self).__init__(connector, path,
                                                     redfish_version)
