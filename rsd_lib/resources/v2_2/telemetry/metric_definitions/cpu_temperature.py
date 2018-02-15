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


class CPUTemperature(base.ResourceBase):

    name = base.Field('Name')
    """The CPUHealth metric definition name"""

    identity = base.Field('Id', required=True)
    """The CPUHealth metric definition identity string"""

    metric_type = base.Field('MetricType')
    """The type of metric"""

    sensor_type = base.Field('SensorType')
    """The type of sensor"""

    implementation = base.Field('Implementation')
    """The implementation type of sensor"""

    sensing_interval = base.Field('SensingInterval')
    """The sensing interval"""

    physical_context = base.Field('PhysicalContext')
    """The physical context of this metric definition"""

    units = base.Field('Units')
    """The units of the sensor"""

    min_reading_range = base.Field('MinReadingRange', adapter=int)
    """The min reading range of this sensor"""

    max_reading_range = base.Field('MaxReadingRange', adapter=int)
    """The max reading range of this sensor"""

    precision = base.Field('Precision', adapter=int)
    """The precision of this sensor"""

    calibration = base.Field('Calibration', adapter=int)
    """The calibration of this sensor"""
