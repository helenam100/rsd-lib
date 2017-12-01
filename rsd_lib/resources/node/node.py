# Copyright 2017 Intel, Inc.
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

from jsonschema import validate
import logging

from sushy import exceptions
from sushy.resources import base
from sushy.resources import common
from sushy.resources.system import system
from sushy import utils

from rsd_lib.resources.node import constants as node_cons
from rsd_lib.resources.node import mappings as node_maps
from rsd_lib.resources.node import schemas as node_schemas


LOG = logging.getLogger(__name__)


class AssembleActionField(base.CompositeField):
    target_uri = base.Field('target', required=True)


class AttachEndpointActionField(base.CompositeField):
    allowed_values = base.Field('Resource@Redfish.AllowableValues',
                                default=[],
                                adapter=utils.get_members_identities)

    target_uri = base.Field('target', required=True)


class DetachEndpointActionField(base.CompositeField):
    allowed_values = base.Field('Resource@Redfish.AllowableValues',
                                default=[],
                                adapter=utils.get_members_identities)

    target_uri = base.Field('target', required=True)


class ComposeNodeActionField(base.CompositeField):
    target_uri = base.Field('target', required=True)


class NodeActionsField(base.CompositeField):
    reset = common.ResetActionField('#ComposedNode.Reset')
    assemble = AssembleActionField('#ComposedNode.Assemble')
    attach_endpoint = AttachEndpointActionField('#ComposedNode.AttachEndpoint')
    detach_endpoint = DetachEndpointActionField('#ComposedNode.DetachEndpoint')


class NodeCollectionActionsField(base.CompositeField):
    compose = ComposeNodeActionField('#ComposedNodeCollection.Allocate')


class StatusField(base.CompositeField):
    state = base.Field('State')
    health = base.Field('Health')
    health_rollup = base.Field('HealthRollup')


class BootField(base.CompositeField):
    allowed_values = base.Field(
        'BootSourceOverrideTarget@Redfish.AllowableValues',
        adapter=list)

    enabled = base.MappedField('BootSourceOverrideEnabled',
                               node_maps.BOOT_SOURCE_ENABLED_MAP)

    mode = base.MappedField('BootSourceOverrideMode',
                            node_maps.BOOT_SOURCE_MODE_MAP)

    target = base.MappedField('BootSourceOverrideTarget',
                              node_maps.BOOT_SOURCE_TARGET_MAP)


class MemorySummaryField(base.CompositeField):
    health = base.Field(['Status', 'Health'])
    """The overall health state of memory.

    This signifies health state of memory along with its dependent resources.
    """

    size_gib = base.Field('TotalSystemMemoryGiB', adapter=int)
    """The size of memory of the node in GiB.

    This signifies the total installed, operating system-accessible memory
    (RAM), measured in GiB.
    """


class ProcessorSummaryField(base.CompositeField):
    health = base.Field(['Status', 'Health'])
    """The overall health state of the node processors."""

    count = base.Field('Count', adapter=int)
    """The number of CPUs in the node."""

    model = base.Field('Model')
    """Basic information about processor model."""


class Node(base.ResourceBase):

    boot = BootField('Boot', required=True)
    """A dictionary containg the current boot device, frequency and mode"""

    composed_node_state = base.MappedField('ComposedNodeState',
                                           node_maps.COMPOSED_NODE_STATE_MAP)
    """Current state of assembly process for this node"""

    description = base.Field('Description')
    """The node description"""

    identity = base.Field('Id', required=True)
    """The node identity string"""

    name = base.Field('Name')
    """The node name"""

    power_state = base.MappedField('PowerState',
                                   node_maps.NODE_POWER_STATE_MAP)
    """The node power state"""

    status = StatusField('Status')
    """The node status"""

    uuid = base.Field('UUID')
    """The node UUID"""

    memory_summary = MemorySummaryField('Memory')
    """The summary info of memory of the node in general detail"""

    processor_summary = ProcessorSummaryField('Processors')
    """The summary info for the node processors in general detail"""

    _system = None  # ref to System instance

    _actions = NodeActionsField('Actions', required=True)

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a ComposedNode

        :param connector: A Connector instance
        :param identity: The identity of the Node resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Node, self).__init__(connector, identity, redfish_version)

    def _get_reset_action_element(self):
        reset_action = self._actions.reset
        if not reset_action:
            raise exceptions.MissingActionError(action='#ComposedNode.Reset',
                                                resource=self._path)
        return reset_action

    def _get_assemble_action_element(self):
        assemble_action = self._actions.assemble
        if not assemble_action:
            raise exceptions.MissingActionError(
                action='#ComposedNode.Assemble',
                resource=self._path)
        return assemble_action

    def get_allowed_reset_node_values(self):
        """Get the allowed values for resetting the node.

        :returns: A set with the allowed values.
        """
        reset_action = self._get_reset_action_element()

        if not reset_action.allowed_values:
            LOG.warning('Could not figure out the allowed values for the '
                        'reset node action for Node %s', self.identity)
            return set(node_maps.RESET_NODE_VALUE_MAP_REV)

        return set([node_maps.RESET_NODE_VALUE_MAP[v] for v in
                    set(node_maps.RESET_NODE_VALUE_MAP).
                    intersection(reset_action.allowed_values)])

    def reset_node(self, value):
        """Reset the node.

        :param value: The target value.
        :raises: InvalidParameterValueError, if the target value is not
            allowed.
        """
        valid_resets = self.get_allowed_reset_node_values()
        if value not in valid_resets:
            raise exceptions.InvalidParameterValueError(
                parameter='value', value=value, valid_values=valid_resets)

        value = node_maps.RESET_NODE_VALUE_MAP_REV[value]
        target_uri = self._get_reset_action_element().target_uri

        self._conn.post(target_uri, data={'ResetType': value})

    def assemble_node(self):
        """Assemble the composed node."""
        target_uri = self._get_assemble_action_element().target_uri

        self._conn.post(target_uri)

    def get_allowed_node_boot_source_values(self):
        """Get the allowed values for changing the boot source.

        :returns: A set with the allowed values.
        """
        if not self.boot.allowed_values:
            LOG.warning('Could not figure out the allowed values for '
                        'configuring the boot source for Node %s',
                        self.identity)
            return set(node_maps.BOOT_SOURCE_TARGET_MAP_REV)

        return set([node_maps.BOOT_SOURCE_TARGET_MAP[v] for v in
                    set(node_maps.BOOT_SOURCE_TARGET_MAP).
                    intersection(self.boot.allowed_values)])

    def set_node_boot_source(self, target,
                             enabled=node_cons.BOOT_SOURCE_ENABLED_ONCE,
                             mode=None):
        """Set the boot source.

        Set the boot source to use on next reboot of the Node.

        :param target: The target boot source.
        :param enabled: The frequency, whether to set it for the next
            reboot only (BOOT_SOURCE_ENABLED_ONCE) or persistent to all
            future reboots (BOOT_SOURCE_ENABLED_CONTINUOUS) or disabled
            (BOOT_SOURCE_ENABLED_DISABLED).
        :param mode: The boot mode, UEFI (BOOT_SOURCE_MODE_UEFI) or
            Legacy (BOOT_SOURCE_MODE_LEGACY).
        :raises: InvalidParameterValueError, if any information passed is
            invalid.
        """
        valid_targets = self.get_allowed_node_boot_source_values()
        if target not in valid_targets:
            raise exceptions.InvalidParameterValueError(
                parameter='target', value=target, valid_values=valid_targets)

        if enabled not in node_maps.BOOT_SOURCE_ENABLED_MAP_REV:
            raise exceptions.InvalidParameterValueError(
                parameter='enabled', value=enabled,
                valid_values=list(node_maps.BOOT_SOURCE_TARGET_MAP_REV))

        data = {
            'Boot': {
                'BootSourceOverrideTarget':
                    node_maps.BOOT_SOURCE_TARGET_MAP_REV[target],
                'BootSourceOverrideEnabled':
                    node_maps.BOOT_SOURCE_ENABLED_MAP_REV[enabled]
            }
        }

        if mode is not None:
            if mode not in node_maps.BOOT_SOURCE_MODE_MAP_REV:
                raise exceptions.InvalidParameterValueError(
                    parameter='mode', value=mode,
                    valid_values=list(node_maps.BOOT_SOURCE_MODE_MAP_REV))

            data['Boot']['BootSourceOverrideMode'] = (
                node_maps.BOOT_SOURCE_MODE_MAP_REV[mode])

        self._conn.patch(self.path, data=data)

    def _get_system_path(self):
        """Helper function to find the System path"""
        system_col = self.json.get('Links').get('ComputerSystem')
        if not system_col:
            raise exceptions.MissingAttributeError(attribute='System',
                                                   resource=self._path)
        return system_col.get('@odata.id')

    @property
    def system(self):
        """Property to provide reference to `System` instance

        It is calculated once the first time it is queried. On refresh,
        this property is reset.
        """
        if self._system is None:
            self._system = system.System(self._conn, self._get_system_path(),
                                         redfish_version=self.redfish_version)

        return self._system

    def _get_attach_endpoint_action_element(self):
        attach_endpoint_action = self._actions.attach_endpoint
        if not attach_endpoint_action:
            raise exceptions.MissingActionError(
                action='#ComposedNode.AttachEndpoint',
                resource=self._path)
        return attach_endpoint_action

    def attach_endpoint(self, endpoint=None, capacity=None):
        """Attach endpoint from available pool to composed node

        :param endpoint: Link to endpoint to attach.
        :param capacity: Requested capacity of the drive in GiB.
        :raises: InvalidParameterValueError
        :raises: BadRequestError if at least one param isn't specified
        """
        attach_action = self._get_attach_endpoint_action_element()
        valid_endpoints = attach_action.allowed_values
        target_uri = attach_action.target_uri

        if endpoint and endpoint not in valid_endpoints:
            raise exceptions.InvalidParameterValueError(
                parameter='endpoint', value=endpoint,
                valid_values=valid_endpoints)

        data = {}
        if endpoint is not None:
            data['Resource'] = {'@odata.id': endpoint}
        if capacity is not None:
            data['CapacityGiB'] = capacity

        self._conn.post(target_uri, data=data)

    def _get_detach_endpoint_action_element(self):
        detach_endpoint_action = self._actions.detach_endpoint
        if not detach_endpoint_action:
            raise exceptions.MissingActionError(
                action='#ComposedNode.DetachEndpoint',
                resource=self._path)
        return detach_endpoint_action

    def detach_endpoint(self, endpoint):
        """Detach already attached endpoint from composed node

        :param endpoint: Link to endpoint to detach
        :raises: InvalidParameterValueError
        :raises: BadRequestError
        """
        detach_action = self._get_detach_endpoint_action_element()
        valid_endpoints = detach_action.allowed_values
        target_uri = detach_action.target_uri

        if endpoint not in valid_endpoints:
            raise exceptions.InvalidParameterValueError(
                parameter='endpoint', value=endpoint,
                valid_values=valid_endpoints)

        data = {'Resource': endpoint}

        self._conn.post(target_uri, data=data)

    def delete_node(self):
        """Delete (disassemble) the node.

        When this action is called several tasks are performed. A graceful
        shutdown is sent to the computer system, all VLANs except reserved ones
        are removed from associated ethernet switch ports, the computer system
        is deallocated and the remote target is deallocated.
        """
        self._conn.delete(self.path)

    def refresh(self):
        super(Node, self).refresh()
        self._system = None


class NodeCollection(base.ResourceCollectionBase):

    _actions = NodeCollectionActionsField('Actions', required=True)

    @property
    def _resource_type(self):
        return Node

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a ComposedNodeCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Node collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(NodeCollection, self).__init__(connector, path,
                                             redfish_version)

    def _get_compose_action_element(self):
        compose_action = self._actions.compose
        if not compose_action:
            raise exceptions.MissingActionError(
                action='#ComposedNodeCollection.Allocate',
                resource=self._path)
        return compose_action

    def _create_compose_request(self, name=None, description=None,
                                processor_req=None, memory_req=None,
                                remote_drive_req=None, local_drive_req=None,
                                ethernet_interface_req=None):

        request = {}

        if name is not None:
            request['Name'] = name
        if description is not None:
            request['Description'] = description

        if processor_req is not None:
            validate(processor_req,
                     node_schemas.processor_req_schema)
            request['Processors'] = processor_req

        if memory_req is not None:
            validate(memory_req,
                     node_schemas.memory_req_schema)
            request['Memory'] = memory_req

        if remote_drive_req is not None:
            validate(remote_drive_req,
                     node_schemas.remote_drive_req_schema)
            request['RemoteDrives'] = remote_drive_req

        if local_drive_req is not None:
            validate(local_drive_req,
                     node_schemas.local_drive_req_schema)
            request['LocalDrives'] = local_drive_req

        if ethernet_interface_req is not None:
            validate(ethernet_interface_req,
                     node_schemas.ethernet_interface_req_schema)
            request['EthernetInterfaces'] = ethernet_interface_req

        return request

    def compose_node(self, name=None, description=None,
                     processor_req=None, memory_req=None,
                     remote_drive_req=None, local_drive_req=None,
                     ethernet_interface_req=None):
        """Compose a node from RackScale hardware

        :param name: Name of node
        :param description: Description of node
        :param processor_req: JSON for node processors
        :param memory_req: JSON for node memory modules
        :param remote_drive_req: JSON for node remote drives
        :param local_drive_req: JSON for node local drives
        :param ethernet_interface_req: JSON for node ethernet ports
        :returns: The location of the composed node
        """
        target_uri = self._get_compose_action_element().target_uri
        properties = self._create_compose_request(
            name=name, description=description,
            processor_req=processor_req,
            memory_req=memory_req,
            remote_drive_req=remote_drive_req,
            local_drive_req=local_drive_req,
            ethernet_interface_req=ethernet_interface_req)
        resp = self._conn.post(target_uri, data=properties)
        LOG.info("Node created at %s", resp.headers['Location'])
        node_url = resp.headers['Location']
        return node_url[node_url.find(self._path):]
