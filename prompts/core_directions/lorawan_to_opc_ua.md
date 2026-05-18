# Prompt: LoRaWAN -> OPC UA

Interaction class: Async -> Async

```text
You are an industrial protocol expert. Based on the complete protocol template information below, generate a standalone protocol conversion script.

[L_arch] ----------------------------------------------------------------
Conversion direction: LoRaWAN -> OPC UA
Architecture: optimal (fully async mode; use a single event loop and await both source-side reads/messages and target-side writes.)

IMPORTANT: this is a UNIDIRECTIONAL converter (LoRaWAN -> OPC UA).
  - read only from LoRaWAN;
  - write only to OPC UA;
  - do NOT subscribe to or poll OPC UA as a source;
  - do NOT implement the reverse flow.

[L_api] -----------------------------------------------------------------
Source protocol template: LoRaWAN
  - Port: 1700
  - Library: aiohttp
  - Imports:
    import aiohttp
    import asyncio
    import json
    import time
  - Client init: session = aiohttp.ClientSession()
  - Connect: # LoRaWAN HTTP API does not require explicit connection
  - Disconnect: await session.close()
  - Read template:
    async with session.get(f"http://{host}:{port}/api/lorawan/devices/{device_id}/data") as response:
        if response.status == 200:
            data = await response.json()
            value = data.get("payload_fields", {}).get("value", data.get("value"))
        else:
            raise Exception(f"LoRaWAN read failed: {response.status}")
  - Write template:
    payload = {"payload_fields": {"value": {value}, "timestamp": time.time()}}
    async with session.post(f"http://{host}:{port}/api/lorawan/devices/{device_id}/data", json=payload) as response:
        if response.status not in [200, 201]:
            raise Exception(f"LoRaWAN write failed: {response.status}")
  - Address format: Device identifier, e.g., device_temp_01.
  - Notes: LoRaWAN is accessed through an HTTP API exposing device payload_fields.

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
"source": "device_temp_01",
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
"source": "device_press_01",
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
"source": "device_valve_01",
"target": "ns=2;i=1003",
"json_path": "",
"array_length": 1,
"element_type": ""
  }
]

[L_ops] -----------------------------------------------------------------
Required structure of the generated Python script:
  1. Imports: union of the two protocol import blocks above.
  2. Server config: LoRaWAN at localhost:1700; OPC UA at localhost:4840.
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
