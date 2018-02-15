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

import os

from sushy.resources import base

from rsd_lib.resources.v2_2.telemetry.metric_definitions import cpu_bandwidth
from rsd_lib.resources.v2_2.telemetry.metric_definitions import cpu_health
from rsd_lib.resources.v2_2.telemetry.metric_definitions import cpu_temperature


class MetricDefinitionsCollection(base.ResourceCollectionBase):

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a MetricDefinitionsCollection

        :param connector: A Connector instance
        :param path: The canonical path to the MetricDefinitions
                     collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(MetricDefinitionsCollection, self).__init__(
            connector, path, redfish_version)

    def _get_metric_definition_type(self, identity):
        """Get metric definition class

        :param identity: The identity of the metric definition
        :returns: The corresponding metric definition class
        """
        metric_def_name = os.path.basename(identity)

        if metric_def_name == 'CPUTemperature':
            return cpu_temperature.CPUTemperature
        elif metric_def_name == 'CPUHealth':
            return cpu_health.CPUHealth
        elif metric_def_name == 'CPUBandwidth':
            return cpu_bandwidth.CPUBandwidth
        else:
            raise NotImplementedError(
                'Metric definition {0} is not supported yet.'
                .format(metric_def_name))

    def get_member(self, identity):
        """Given the identity return a metric definition object

        :param identity: The identity of the metric definition
        :returns: The metric definition object
        :raises: ResourceNotFoundError
        """
        # return cpu_temperature.CPUTemperature(
        #     self._conn, identity, redfish_version=self.redfish_version)
        metric_definition_type = self._get_metric_definition_type(identity)
        return metric_definition_type(self._conn, identity,
                                      redfish_version=self.redfish_version)

    @property
    def _resource_type(self):
        pass
