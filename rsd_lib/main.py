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

from distutils import version

from sushy import connector
from sushy.resources import base

from rsd_lib.resources import v2_1
from rsd_lib.resources import v2_2


class RSDLib(base.ResourceBase):

    _redfish_version = base.Field(['RedfishVersion'], required=True)
    """FabricCollection path"""

    _rsd_api_version = base.Field(['Oem', 'Intel_RackScale', 'ApiVersion'],
                                  required=True)
    """RSD API version"""

    def __init__(self, base_url, username=None, password=None,
                 root_prefix='/redfish/v1/', verify=True):
        """A class representing a RootService

        :param base_url: The base URL to the Redfish controller. It
            should include scheme and authority portion of the URL. For
            example: https://mgmt.vendor.com
        :param username: User account with admin/server-profile access
            privilege
        :param password: User account password
        :param root_prefix: The default URL prefix. This part includes
            the root service and version. Defaults to /redfish/v1
        :param verify: Either a boolean value, a path to a CA_BUNDLE
            file or directory with certificates of trusted CAs. If set to
            True the driver will verify the host certificates; if False
            the driver will ignore verifying the SSL certificate; if it's
            a path the driver will use the specified certificate or one of
            the certificates in the directory. Defaults to True.
        """
        self._root_prefix = root_prefix
        super(RSDLib, self).__init__(
            connector.Connector(base_url, username, password, verify),
            path=self._root_prefix)

    def factory(self):
        """Return different resource module according to RSD API Version

        :returns: a resource module
        """
        rsd_version = version.StrictVersion(self._rsd_api_version)
        if rsd_version < version.StrictVersion("2.2.0"):
            # Use the interface of RSD API 2.1.0 to interact with RSD 2.1.0 and
            # all previous version.
            return v2_1.RSDLibV2_1(self._conn, self._root_prefix,
                                   redfish_version=self._redfish_version)
        elif version.StrictVersion("2.2.0") <= rsd_version \
            and rsd_version < version.StrictVersion("2.3.0"):
            # Specific interface for RSD 2.2 version
            return v2_2.RSDLibV2_2(self._conn, self._root_prefix,
                                   redfish_version=self._redfish_version)
        else:
            raise NotImplementedError(
                "The rsd-lib library doesn't support RSD API "
                "version {0}.".format(self._rsd_api_version))
