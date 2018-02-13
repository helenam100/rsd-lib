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


class ProcessorMetrics(base.ResourceBase):
    name = base.Field('Name')
    """The metrics name"""

    description = base.Field('Description')
    """The metrics description"""

    identity = base.Field('Id')
    """The metrics identity"""

    average_frequency_mhz = base.Field('AverageFrequencyMHz', adapter=int)
    """The processor average frequency mhz"""

    throttling_celsius = base.Field('ThrottlingCelsius', adapter=int)
    """The processor throttling celsius"""

    temperature_celsius = base.Field('TemperatureCelsius', adapter=int)
    """The processor temperature celsius"""

    consumed_power_watt = base.Field('ConsumedPowerWatt', adapter=int)
    """The processor consumed power watt"""

    health = base.Field('Health', adapter=list)
    """The detail health information"""
