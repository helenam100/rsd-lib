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

from sushy.resources import base


class Metrics(base.ResourceBase):
    name = base.Field('Name')
    """The metrics name"""

    description = base.Field('Description')
    """The metrics description"""

    identity = base.Field('Id')
    """The metrics identity"""

    processor_bandwidth_percent = base.Field('ProcessorBandwidthPercent',
                                             adapter=int)
    """The processor bandwidth percent"""

    memory_bandwidth_percent = base.Field('MemoryBandwidthPercent',
                                          adapter=int)
    """The memory bandwidth percent"""

    memory_throttled_cycles_percent = base.Field(
        'MemoryThrottledCyclesPercent', adapter=int)
    """The memory throttled cycles percent"""

    processor_power_watt = base.Field('ProcessorPowerWatt', adapter=int)
    """The processor power watt"""

    memory_power_watt = base.Field('MemoryPowerWatt', adapter=int)
    """The memory power watt"""

    io_bandwidth_gbps = base.Field('IOBandwidthGBps', adapter=int)
    """The io bandwidth GBps"""

    health = base.Field('Health', adapter=list)
    """The detail health information"""
