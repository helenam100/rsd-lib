# Copyright (c) 2018 Intel, Corp.
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

capacity_req_schema = {
    'type': 'number'
}

access_capabilities_req_schema = {
    'type': 'array',
    'items': {
        'type': 'string',
        'enum': ['Read', 'Write', 'WriteOnce', 'Append', 'Streaming']
    }
}

capacity_sources_req_schema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'ProvidingPools': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        '@odata.id': {'type': 'string'}
                    },
                    'additionalProperties': False
                }
            }
        },
        'additionalProperties': False
    }
}

replica_infos_req_schema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'ReplicaType': {'type': 'string'},
            'Replica': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            }
        },
        'additionalProperties': False
    }
}

bootable_req_schema = {
    'type': 'boolean'
}
