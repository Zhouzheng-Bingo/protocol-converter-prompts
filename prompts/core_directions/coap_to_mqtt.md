# Prompt: CoAP -> MQTT

Interaction class: Async -> Async

```text
You are an industrial protocol expert. Based on the complete protocol template information below, generate a standalone protocol conversion script.

[L_arch] ----------------------------------------------------------------
Conversion direction: CoAP -> MQTT
Architecture: optimal (fully async mode; use a single event loop and await both source-side reads/messages and target-side writes.)

IMPORTANT: this is a UNIDIRECTIONAL converter (CoAP -> MQTT).
  - read only from CoAP;
  - write only to MQTT;
  - do NOT subscribe to or poll MQTT as a source;
  - do NOT implement the reverse flow.

[L_api] -----------------------------------------------------------------
Source protocol template: CoAP
  - Port: 5683
  - Library: aiocoap
  - Imports:
    import asyncio
    from aiocoap import Context, Message, PUT, GET
    import json
  - Client init: context = await Context.create_client_context()
  - Connect: # CoAP does not require an explicit connection step
  - Disconnect: await context.shutdown()
  - Read template:
    request = Message(code=GET, uri=f"coap://{host}:{port}{uri}")
    response = await context.request(request).response
    if response.code.is_successful():
        data = json.loads(response.payload.decode())
        value = data.get("value")
    else:
        raise Exception(f"CoAP read failed: {response.code}")
  - Write template:
    payload = json.dumps({"value": {value}}).encode()
    request = Message(code=PUT, uri=f"coap://{host}:{port}{uri}", payload=payload)
    response = await context.request(request).response
    if not response.code.is_successful():
        raise Exception(f"CoAP write failed: {response.code}")
  - Address format: URI path, e.g., /sensors/temp.
  - Notes: CoAP is represented through aiocoap and is executed in an async event loop.

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
"source": "/sensors/temp",
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
"source": "/sensors/pressure",
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
"source": "/actuators/valve",
"target": "actuators/valve/01",
"json_path": "",
"array_length": 1,
"element_type": ""
  }
]

[L_ops] -----------------------------------------------------------------
Required structure of the generated Python script:
  1. Imports: union of the two protocol import blocks above.
  2. Server config: CoAP at localhost:5683; MQTT at localhost:1883.
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
