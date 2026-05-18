# Prompt: OPC UA -> HTTP

Interaction class: Async -> Sync

```text
You are an industrial protocol expert. Based on the complete protocol template information below, generate a standalone protocol conversion script.

[L_arch] ----------------------------------------------------------------
Conversion direction: OPC UA -> HTTP
Architecture: optimal (mixed mode: async source + sync target; use async def main(), await source reads/messages, and call target synchronous writes directly in controlled blocks.)

IMPORTANT: this is a UNIDIRECTIONAL converter (OPC UA -> HTTP).
  - read only from OPC UA;
  - write only to HTTP;
  - do NOT subscribe to or poll HTTP as a source;
  - do NOT implement the reverse flow.

[L_api] -----------------------------------------------------------------
Source protocol template: OPC UA
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

Target protocol template: HTTP
  - Port: 8080
  - Library: requests
  - Imports:
    import requests
    import json
    import time
  - Client init: session = requests.Session()
  - Connect: # HTTP does not require an explicit connection step
  - Disconnect: session.close()
  - Read template:
    response = session.get("http://{host}:{port}{endpoint}")
    if response.status_code == 200:
        data = response.json()
        value = data.get("{field}", data.get("value"))
    else:
        raise Exception(f"HTTP read failed: {response.status_code}")
  - Write template:
    payload = {"field": "{semantic_name}", "value": {value}}
    response = session.post("http://{host}:{port}{endpoint}", json=payload)
    if response.status_code not in [200, 201]:
        raise Exception(f"HTTP write failed: {response.status_code}")
  - Address format: REST endpoint path, e.g., /api/sensors/temperature.
  - Notes: Request/response API; use JSON payloads and explicit status-code checks.

[L_map] -----------------------------------------------------------------
Address mappings (JSON, extracted from AddressMapping nodes):
[
  {
"semantic_name": "temperature_sensor_01",
"description": "temperature sensor",
"data_type": "float",
"unit": "C",
"source": "ns=2;i=1001",
"target": "/api/sensors/temperature",
"json_path": "",
"array_length": 1,
"element_type": ""
  },
  {
"semantic_name": "pressure_sensor_01",
"description": "pressure sensor",
"data_type": "float",
"unit": "kPa",
"source": "ns=2;i=1002",
"target": "/api/sensors/pressure",
"json_path": "",
"array_length": 1,
"element_type": ""
  },
  {
"semantic_name": "valve_control_01",
"description": "valve opening",
"data_type": "int",
"unit": "%",
"source": "ns=2;i=1003",
"target": "/api/actuators/valve",
"json_path": "",
"array_length": 1,
"element_type": ""
  }
]

[L_ops] -----------------------------------------------------------------
Required structure of the generated Python script:
  1. Imports: union of the two protocol import blocks above.
  2. Server config: OPC UA at localhost:4840; HTTP at localhost:8080.
  3. Client setup: use the Client init templates above.
  4. Connections: use the Connect / Disconnect code above.
  5. Core loop: follow the selected architecture; convert each mapping item from source to target; log every read/write; catch and log errors per item.
  6. main(): include complete error handling and cleanup.
  7. Entry point: include a directly runnable Python entry point.

Adaptation guidance: mixed mode: async source + sync target; use async def main(), await source reads/messages, and call target synchronous writes directly in controlled blocks.
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
