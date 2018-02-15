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
from sushy.resources.system import system

from rsd_lib.resources.v2_1.system import memory
from rsd_lib import utils


class System(system.System):

    _memory = None  # ref to System memory collection instance

    def _get_memory_collection_path(self):
        """Helper function to find the memory path"""
        system_col = self.json.get('Memory')
        if not system_col:
            raise exceptions.MissingAttributeError(attribute='Memory',
                                                   resource=self._path)
        return utils.get_resource_identity(system_col)

    @property
    def memory(self):
        """Property to provide reference to `Metrics` instance

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
        self._memory = None


class SystemCollection(system.SystemCollection):

    @property
    def _resource_type(self):
        return System
