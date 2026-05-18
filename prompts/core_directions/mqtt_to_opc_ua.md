# Prompt: MQTT -> OPC UA

Interaction class: Async -> Async

```text
You are an industrial protocol expert. Based on the complete protocol template information below, generate a standalone protocol conversion script.

[L_arch] ----------------------------------------------------------------
Conversion direction: MQTT -> OPC UA
Architecture: optimal (fully async mode; use a single event loop and await both source-side reads/messages and target-side writes.)

IMPORTANT: this is a UNIDIRECTIONAL converter (MQTT -> OPC UA).
  - read only from MQTT;
  - write only to OPC UA;
  - do NOT subscribe to or poll OPC UA as a source;
  - do NOT implement the reverse flow.

[L_api] -----------------------------------------------------------------
Source protocol template: MQTT
  - Port: 1883
  - Library: aiomqtt
  - Imports:
    import aiomqtt
    import asyncio
    import json
    import time
  - Client init: aiomqtt.Client(hostname='{host}', port={port})
  - Connect: # use async with aiomqtt.Client(...) for connection management
  - Disconnect: # async context manager disconnects automatically
  - Read template:
    async with aiomqtt.Client(hostname='{host}', port={port}) as client:
        await client.subscribe('{address}')
        async for message in client.messages:
            payload = json.loads(message.payload.decode())
  - Write template:
    payload = json.dumps({'value': {value}, 'timestamp': time.time()})
    await client.publish('{address}', payload)
  - Address format: MQTT topic string, e.g., sensors/temperature/01.
  - Notes: Publish/subscribe protocol; when used as source, use event-driven message handling and process all mappings matching the topic.

Target protocol template: OPC UA
  - Port: 4840
  - Library: asyncua
  - Imports:
    from asyncua import Client, ua
    import asyncio
    import logging
  - Client init: client = Client('{url}')
  - Connect: await client.connect()
  - Disconnect: await client.disconnect()
  - Read template:
    node = client.get_node('{address}')
    value = await node.read_value()
    if value is None:
        raise Exception(f'Read OPC UA node {address} failed')
  - Write template:
    node = client.get_node('{address}')
    await node.write_value(ua.Variant({value}, ua.VariantType.{variant_type}))
  - Address format: NodeId string, e.g., ns=2;i=1001.
  - Notes: Use ua.Variant with the type-specific VariantType when writing OPC UA values.

[L_map] -----------------------------------------------------------------
Address mappings (JSON, extracted from AddressMapping nodes):
[
  {
"semantic_name": "temperature_sensor_01",
"description": "temperature sensor",
"data_type": "Float",
"unit": "C",
"source": "sensors/temperature/01",
"target": "ns=2;i=1001",
"json_path": "",
"array_length": 1,
"element_type": ""
  },
  {
"semantic_name": "pressure_sensor_01",
"description": "pressure sensor",
"data_type": "Float",
"unit": "kPa",
"source": "sensors/pressure/01",
"target": "ns=2;i=1002",
"json_path": "",
"array_length": 1,
"element_type": ""
  },
  {
"semantic_name": "valve_control_01",
"description": "valve opening",
"data_type": "UInt16",
"unit": "%",
"source": "actuators/valve/01",
"target": "ns=2;i=1003",
"json_path": "",
"array_length": 1,
"element_type": ""
  }
]

[L_ops] -----------------------------------------------------------------
Required structure of the generated Python script:
  1. Imports: union of the two protocol import blocks above.
  2. Server config: MQTT at localhost:1883; OPC UA at localhost:4840.
  3. Client setup: use the Client init templates above.
  4. Connections: use the Connect / Disconnect code above.
  5. Core loop: follow the selected architecture; convert each mapping item from source to target; log every read/write; catch and log errors per item.
  6. main(): include complete error handling and cleanup.
  7. Entry point: include a directly runnable Python entry point.

Adaptation guidance: fully async mode; use a single event loop and await both source-side reads/messages and target-side writes.
Protocol-specific hints: source notes and target notes above are ground truth.
General: follow the chosen architecture strictly; use the templates above as ground truth; log every conversion step.

[FA Constraints -- appended when function enhancement is enabled] ------
CRITICAL: strictly follow the provided templates. Do NOT substitute API calls from training knowledge.
  pymodbus 3.x: count MUST be a keyword argument.
  correct: client.read_holding_registers(address=address_offset, count=N, slave=1)
  wrong:   client.read_holding_registers(address_offset, N, slave=1)
Copy the read/write template structure; only substitute the {address}, {value}, {data_type}, and protocol-specific placeholders.
Preserve struct operations, address-offset calculations, and error handling as shown.
```
