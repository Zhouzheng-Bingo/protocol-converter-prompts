# Prompt: LoRaWAN -> MQTT

Interaction class: Async -> Async

```text
You are an industrial protocol expert. Based on the complete protocol template information below, generate a standalone protocol conversion script.

[L_arch] ----------------------------------------------------------------
Conversion direction: LoRaWAN -> MQTT
Architecture: optimal (fully async mode; use a single event loop and await both source-side reads/messages and target-side writes.)

IMPORTANT: this is a UNIDIRECTIONAL converter (LoRaWAN -> MQTT).
  - read only from LoRaWAN;
  - write only to MQTT;
  - do NOT subscribe to or poll MQTT as a source;
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

Target protocol template: MQTT
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

[L_map] -----------------------------------------------------------------
Address mappings (JSON, extracted from AddressMapping nodes):
[
  {
"semantic_name": "temperature_sensor_01",
"description": "temperature sensor",
"data_type": "float",
"unit": "C",
"source": "device_temp_01",
"target": "sensors/temperature/01",
"json_path": "",
"array_length": 1,
"element_type": ""
  },
  {
"semantic_name": "pressure_sensor_01",
"description": "pressure sensor",
"data_type": "float",
"unit": "kPa",
"source": "device_press_01",
"target": "sensors/pressure/01",
"json_path": "",
"array_length": 1,
"element_type": ""
  },
  {
"semantic_name": "valve_control_01",
"description": "valve opening",
"data_type": "int",
"unit": "%",
"source": "device_valve_01",
"target": "actuators/valve/01",
"json_path": "",
"array_length": 1,
"element_type": ""
  }
]

[L_ops] -----------------------------------------------------------------
Required structure of the generated Python script:
  1. Imports: union of the two protocol import blocks above.
  2. Server config: LoRaWAN at localhost:1700; MQTT at localhost:1883.
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
