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


class MetricDefinition(base.ResourceBase):

    name = base.Field('Name')
    """The CPUHealth metric definition name"""

    identity = base.Field('Id', required=True)
    """The CPUHealth metric definition identity string"""

    sensor_type = base.Field('SensorType')
    """The type of sensor"""

    metric_type = base.Field('MetricType')
    """The type of metric"""

    implementation = base.Field('Implementation')
    """The implementation type of sensor"""

    sensing_interval = base.Field('SensingInterval')
    """The sensing interval"""

    physical_context = base.Field('PhysicalContext')
    """The physical context of this metric definition"""

    units = base.Field('Units')
    """The units of the sensor"""

    min_reading_range = base.Field('MinReadingRange')
    """The min reading range of this sensor"""

    max_reading_range = base.Field('MaxReadingRange')
    """The max reading range of this sensor"""

    discrete_values = base.Field('DiscreteValues', adapter=list)
    """The allowed discrete values"""

    precision = base.Field('Precision')
    """The precision of the sensor"""

    calibration = base.Field('Calibration')
    """The calibration of the sensor"""

    isLinear = base.Field('IsLinear', adapter=bool)
    """The boolean indicate this sensor is linear or not"""

    calculable = base.Field('Calculable', adapter=bool)
    """The variable indicate this sensor is calculable or not"""

    data_type = base.Field('DataType')
    """The type of the sensor data"""

    accuracy = base.Field('Accuracy')
    """The accuracy of the sensor"""

    time_stamp_accuracy = base.Field('TimeStampAccuracy')
    """The time stamp accuracy of the sensor"""

    calculation_time_interval = base.Field('CalculationTimeInterval')
    """The calculation time interval of the sensor"""

    calculation_algorithm = base.Field('CalculationAlgorithm')
    """The calculation algorithm of the sensor"""

    calculation_parameters = base.Field('CalculationParameters', adapter=list)
    """The calculation parameters of the sensor"""

    wildcards = base.Field('Wildcards', adapter=list)
    """The wildcards of the sensor"""


class MetricDefinitionsCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return MetricDefinition
