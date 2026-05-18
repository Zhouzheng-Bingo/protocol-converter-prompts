# Prompt: Modbus TCP -> HTTP

Interaction class: Sync -> Sync

```text
You are an industrial protocol expert. Based on the complete protocol template information below, generate a standalone protocol conversion script.

[L_arch] ----------------------------------------------------------------
Conversion direction: Modbus TCP -> HTTP
Architecture: optimal (fully sync mode; use a simple polling loop with synchronous source reads and target writes.)

IMPORTANT: this is a UNIDIRECTIONAL converter (Modbus TCP -> HTTP).
  - read only from Modbus TCP;
  - write only to HTTP;
  - do NOT subscribe to or poll HTTP as a source;
  - do NOT implement the reverse flow.

[L_api] -----------------------------------------------------------------
Source protocol template: Modbus TCP
  - Port: 502
  - Library: pymodbus
  - Imports:
    from pymodbus.client import ModbusTcpClient
    import struct
    import time
  - Client init: client = ModbusTcpClient(host='{host}', port={port})
  - Connect: client.connect()
  - Disconnect: client.close()
  - Read template:
    address_offset = {address} - 40001
    result = client.read_holding_registers(address=address_offset, count=2 if '{data_type}' == 'FLOAT32' else 1, slave=1)
    if not result.isError():
        if '{data_type}' == 'FLOAT32':
            value = struct.unpack('>f', struct.pack('>HH', result.registers[0], result.registers[1]))[0]
        else:
            value = result.registers[0]
    else:
        raise Exception(f'Read Modbus {address} failed: {result}')
  - Write template:
    address_offset = {address} - 40001
    if '{data_type}' == 'FLOAT32':
        high, low = struct.unpack('>HH', struct.pack('>f', float({value})))
        result = client.write_registers(address=address_offset, values=[high, low], slave=1)
    else:
        result = client.write_register(address=address_offset, value=int({value}), slave=1)
    if result.isError():
        raise Exception(f'Write Modbus {address} failed')
  - Address format: 40001-style holding-register address; subtract 40001 to obtain the register offset.
  - Notes: FLOAT32 occupies two consecutive 16-bit registers; use big-endian struct packing/unpacking.

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
"source": "40001",
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
"source": "40004",
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
"source": "40003",
"target": "/api/actuators/valve",
"json_path": "",
"array_length": 1,
"element_type": ""
  }
]

[L_ops] -----------------------------------------------------------------
Required structure of the generated Python script:
  1. Imports: union of the two protocol import blocks above.
  2. Server config: Modbus TCP at localhost:502; HTTP at localhost:8080.
  3. Client setup: use the Client init templates above.
  4. Connections: use the Connect / Disconnect code above.
  5. Core loop: follow the selected architecture; convert each mapping item from source to target; log every read/write; catch and log errors per item.
  6. main(): include complete error handling and cleanup.
  7. Entry point: include a directly runnable Python entry point.

Adaptation guidance: fully sync mode; use a simple polling loop with synchronous source reads and target writes.
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
