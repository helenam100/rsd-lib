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

from rsd_lib.resources.v2_1.system import system
from rsd_lib.resources.v2_2.system import memory
from rsd_lib.resources.v2_2.system import metrics
from rsd_lib.resources.v2_2.system import processor
from rsd_lib import utils


class System(system.System):

    _metrics = None  # ref to System metrics instance
    _processors = None  # ref to ProcessorCollection instance
    _memory = None  # ref to ProcessorCollection instance

    def _get_metrics_path(self):
        """Helper function to find the System metrics path"""
        metrics = self.json.get('Oem').get('Intel_RackScale').get('Metrics')
        if not metrics:
            raise exceptions.MissingAttributeError(attribute='Metrics',
                                                   resource=self._path)
        return utils.get_resource_identity(metrics)

    @property
    def metrics(self):
        """Property to provide reference to `Metrics` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        if self._metrics is None:
            self._metrics = metrics.Metrics(
                self._conn, self._get_metrics_path(),
                redfish_version=self.redfish_version)

        return self._metrics

    @property
    def processors(self):
        """Property to provide reference to `ProcessorCollection` instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._processors is None:
            self._processors = processor.ProcessorCollection(
                self._conn, self._get_processor_collection_path(),
                redfish_version=self.redfish_version)

        return self._processors

    @property
    def memory(self):
        """Property to provide reference to `Memory` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        if self._memory is None:
            self._memory = memory.MemoryCollection(
                self._conn, self._get_memory_collection_path(),
                redfish_version=self.redfish_version)

        return self._memory

    def refresh(self):
        super(System, self).refresh()
        self._metrics = None
        self._processors = None
        self._memory = None


class SystemCollection(system.SystemCollection):

    @property
    def _resource_type(self):
        return System
