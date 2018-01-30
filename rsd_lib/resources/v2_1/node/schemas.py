# Copyright (c) 2017 Intel, Corp.
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

processor_req_schema = {
    'type': 'array',
    'items': [{
        'type': 'object',
        'properties': {
            'Model': {'type': 'string'},
            'TotalCores': {'type': 'number'},
            'AchievableSpeedMHz': {'type': 'number'},
            'InstructionSet': {
                'type': 'string',
                'enum': ['x86', 'x86-64', 'IA-64', 'ARM-A32',
                         'ARM-A64', 'MIPS32', 'MIPS64', 'OEM']
            },
            'Resource': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            },
            'Chassis': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            }
        },
        'additionalProperties': False,
    }]
}

memory_req_schema = {
    'type': 'array',
    'items': [{
        'type': 'object',
        'properties': {
            'CapacityMiB': {'type': 'number'},
            'MemoryDeviceType': {
                'type': 'string',
                'enum': ['DDR', 'DDR2', 'DDR3', 'DDR4', 'DDR4_SDRAM',
                         'DDR4E_SDRAM', 'LPDDR4_SDRAM', 'DDR3_SDRAM',
                         'LPDDR3_SDRAM', 'DDR2_SDRAM', 'DDR2_SDRAM_FB_DIMM',
                         'DDR2_SDRAM_FB_DIMM_PROBE', 'DDR_SGRAM',
                         'DDR_SDRAM', 'ROM', 'SDRAM', 'EDO',
                         'FastPageMode', 'PipelinedNibble']
            },
            'SpeedMHz': {'type': 'number'},
            'Manufacturer': {'type': 'string'},
            'DataWidthBits': {'type': 'number'},
            'Resource': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            },
            'Chassis': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            }
        },
        'additionalProperties': False,
    }]
}

remote_drive_req_schema = {
    'type': 'array',
    'items': [{
        'type': 'object',
        'properties': {
            'CapacityGiB': {'type': 'number'},
            'iSCSIAddress': {'type': 'string'},
            'Master': {
                'type': 'object',
                'properties': {
                    'Type': {
                        'type': 'string',
                        'enum': ['Snapshot', 'Clone']
                    },
                    'Address': {
                        'type': 'object',
                        'properties': {
                            '@odata.id': {'type': 'string'}
                        }
                    }
                }
            }
        },
        'additionalProperties': False,
    }]
}

local_drive_req_schema = {
    'type': 'array',
    'items': [{
        'type': 'object',
        'properties': {
            'CapacityGiB': {'type': 'number'},
            'Type': {
                'type': 'string',
                'enum': ['HDD', 'SSD']
            },
            'MinRPM': {'type': 'number'},
            'SerialNumber': {'type': 'string'},
            'Interface': {
                'type': 'string',
                'enum': ['SAS', 'SATA', 'NVMe']
            },
            'Resource': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            },
            'Chassis': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            },
            'FabricSwitch': {'type': 'boolean'}
        },
        'additionalProperties': False,
    }]
}

ethernet_interface_req_schema = {
    'type': 'array',
    'items': [{
        'type': 'object',
        'properties': {
            'SpeedMbps': {'type': 'number'},
            'PrimaryVLAN': {'type': 'number'},
            'VLANs': {
                'type': 'array',
                'additionalItems': {
                    'type': 'object',
                    'properties': {
                        'VLANId': {'type': 'number'},
                        'Tagged': {'type': 'boolean'}
                    }
                }
            },
            'Resource': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            },
            'Chassis': {
                'type': 'object',
                'properties': {
                    '@odata.id': {'type': 'string'}
                }
            }
        },
        'additionalProperties': False,
    }]
}
