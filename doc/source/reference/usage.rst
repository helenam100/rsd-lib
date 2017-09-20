.. _usage:

Using rsd-lib
=============

----------------------------------
Composing and using a logical node
----------------------------------

.. code-block:: python

  import rsd_lib

  # Get a connection with the RSD endpoint
  rsd = rsd_lib.RSDLib('http://localhost:8443/redfish/v1',
                       username='foo', password='bar')

  # Get the node collection object
  node_col = rsd.get_node_collection()

  # Get a list of existing composed nodes
  node_col.get_members()

  # Compose a new node with no requirements specified
  node1 = node_col.compose_node()

  # Compose a new node specifying requirements
  node2 = node_col.compose_node(
    name='testnode',
    description='this is a node',
    processor_req=[
      {
        'TotalCores': 4
      }],
    memory_req=[
      {
        'CapacityMiB': 8000,
        'MemoryDeviceType': 'DDR'
      }],
    remote_drive_req=[
      {
        'CapacityGiB': 80,
        'iSCSIAddress': 'iqn.oem.com:42',
        'Master': {
          'Type': 'Snapshot',
          'Resource': '/redfish/v1/Services/1/LogicalDrives/1'
        }
      }]
    )

  # Get the python object for the node we created
  node_inst = rsd.get_node(node1)

  # Assemble the composed node (After allocation, node must be assembled)
  node_inst.assemble_node()

  # Refresh the node object
  node_inst.refresh()

  # Get composed node state of node, should be 'assembled'
  print(node_inst.composed_node_state)

  # Power the node ON
  node_inst.reset_node(rsd_lib.RESET_ON)

  # Get a list of allowed reset values
  print(node_inst.get_allowed_reset_node_values())

  # Refresh the node object
  node_inst.refresh()

  # Get the current power state
  print(node_inst.power_state)

  # Set the next boot device to boot once from PXE in UEFI mode
  node_inst.set_node_boot_source(rsd_lib.BOOT_SOURCE_TARGET_PXE,
                                 enabled=rsd_lib.BOOT_SOURCE_ENABLED_ONCE,
                                 mode=rsd_lib.BOOT_SOURCE_MODE_UEFI)

  # Get the current boot source information
  print(node_inst.boot)

  # Get a list of allowed boot source target values
  print(node_inst.get_allowed_node_boot_source_values())

  # Get the memory summary
  print(node_inst.memory_summary)

  # Get the processor summary
  print(node_inst.processor_summary)

  # Delete/Deallocate the composed node
  node_inst.delete_node()

-----------------------------------
Discovering Remote Storage Services
-----------------------------------

  # Get the storage service collection object
  storage_service_col = rsd.get_storage_service_collection()

  # Get storage service instance
  storage_service = storage_service_col.get_members()[0]

  # Get storage service instance with ID
  storage_service2 = rsd.get_storage_service(storage_service.identity)

  # Get physical drives contained by storage service
  physical_drive_col = storage_service.physical_drives()

  Get a physical drive from the collection
  physical_drive = physical_drive_col.get_members()[0]

  # Get capacity of the physical drive
  print(physical_drive.capacity_gib)

  # Get logical drives contained by storage service
  logical_drive_col = storage_service.logical_drives()

  # Get logical drive
  logical_drive = logical_drive_col.get_members()[0]

  # Get type of a logical drive
  print(logical_drive.drive_type)

  # Get remote target collection
  remote_target_col = storage_service.remote_targets()

  # Get remote target instance
  target = remote_target_col.get_members()[0]

  # Get Initiator IQN of a remote target
  print(target.initiators[0].iscsi.iqn)

----------------------------------------------------
Discovering NVMe Devices and Attaching them to Nodes
----------------------------------------------------

  # Get the fabric collection object
  fabric_col = rsd.get_fabric_collection()

  # Get fabric instance
  fabric = fabric_col.get_members()[0]

  # Get a fabric instance with an ID
  fabric2 = rsd.get_fabric(fabric.identity)

  # Get endpoint collection
  endpoint_col = fabric.endpoints()

  # Get endpoint instance
  endpoint = endpoint_col.get_members()[0]

  # Get type of connected entity
  print(endpoint.connected_entities[0].entity_type)

  # Get link to entity
  drive_link = endpoint.connected_entities[0].entity_link

  # Get a composed node instance
  node_inst = node_col.get_members()[0]

  # Attach the endpoint to the composed node
  node_inst.attach_endpoint(endpoint=drive_link)

  # Detach the endpoint from the composed node
  node_inst.detach_endpoint(endpoint=drive_link)
