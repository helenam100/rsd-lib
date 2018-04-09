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

from sushy import exceptions

from rsd_lib.resources.v2_1.node import node as v2_1_node


class Node(v2_1_node.Node):

    def attach_endpoint(self, endpoint, protocol=None):
        """Attach endpoint from available pool to composed node

        :param endpoint: Link to endpoint to attach.
        :param protocol: Protocol of the remote drive.
        :raises: InvalidParameterValueError
        """
        attach_action = self._get_attach_endpoint_action_element()
        valid_endpoints = attach_action.allowed_values
        target_uri = attach_action.target_uri

        if endpoint and endpoint not in valid_endpoints:
            raise exceptions.InvalidParameterValueError(
                parameter='endpoint', value=endpoint,
                valid_values=valid_endpoints)

        data = {}
        if endpoint is not None:
            data['Resource'] = {'@odata.id': endpoint}
        if protocol is not None:
            data['Protocol'] = protocol

        self._conn.post(target_uri, data=data)
