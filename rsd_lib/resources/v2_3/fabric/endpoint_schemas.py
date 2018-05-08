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

identifiers_req_schema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'DurableNameFormat': {
                'type': 'string',
                'enum': ['NQN', 'iQN']
            },
            'DurableName': {'type': 'string'}
        },
        "required": ['DurableNameFormat', 'DurableName'],
        'additionalProperties': False
    }
}

connected_entities_req_schema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'EntityLink': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                },
                "required": ['@odata.id'],
                'additionalProperties': False
            },
            'EntityRole': {
                'type': 'string',
                'enum': ['Initiator', 'Target', 'Both']
            },
            'Identifiers': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'DurableNameFormat': {
                            'type': 'string',
                            'enum': ['NQN', 'iQN', 'FC_WWN', 'UUID', 'EUI',
                                     'NAA', 'NSID', 'SystemPath', 'LUN']
                        },
                        'DurableName': {'type': 'string'}
                    },
                    "required": ['DurableNameFormat', 'DurableName'],
                    'additionalProperties': False
                }
            }
        },
        "required": ['EntityLink', 'EntityRole'],
        'additionalProperties': False
    }
}

protocol_req_schema = {
    'type': 'string',
    'enum': ['NVMeOverFabrics', 'iSCSI']
}

ip_transport_details_req_schema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'TransportProtocol': {'type': 'string'},
            'IPv4Address': {
                'type': 'object',
                'properties': {
                    'Address': {'type': 'string'}
                },
                'additionalProperties': False
            },
            'IPv6Address': {
                'type': 'object',
                'properties': {
                    'Address': {'type': 'string'}
                },
                'additionalProperties': False
            },
            'Port': {'type': 'number'}
        },
        'additionalProperties': False
    }
}

interface_req_schema = {
    'type': 'string'
}

authentication_req_schema = {
    'type': 'object',
    'properties': {
        'Username': {'type': 'string'},
        'Password': {'type': 'string'}
    },
    'additionalProperties': False
}
