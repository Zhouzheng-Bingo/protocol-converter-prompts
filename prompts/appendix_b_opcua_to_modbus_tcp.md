# Appendix B Representative Prompt Excerpt

This is the translated representative prompt excerpt for the OPC UA -> Modbus TCP direction under the `optimal` architecture, matching the manuscript Appendix B in content.

```text
You are an industrial protocol expert. Based on the complete protocol
template information below, generate a standalone protocol conversion
script.

[L_arch] ----------------------------------------------------------------
Conversion direction: OPC UA -> Modbus TCP
Architecture: optimal  (mixed mode: async source + sync target)
  - OPC UA is natively asynchronous (library: asyncua);
  - Modbus TCP is natively synchronous (library: pymodbus);
  - use `async def main()`; await async reads; call sync writes directly;
  - no bridge or message queue required.

IMPORTANT: this is a UNIDIRECTIONAL converter (OPC UA -> Modbus TCP).
  - read only from OPC UA;
  - write only to Modbus TCP;
  - do NOT subscribe to Modbus; do NOT implement the reverse flow.

[L_api] -----------------------------------------------------------------
Source protocol template: OPC UA
  - Port: 4840
  - Library: asyncua
  - Imports:
        from asyncua import Client, ua
        import asyncio
        import logging
  - Client init:   Client('{host}:{port}')
  - Connect:       await client.connect()
  - Disconnect:    await client.disconnect()
  - Read template:
        node = client.get_node('{address}')
        value = await node.read_value()
        if value is None:
            raise Exception(f"Read OPC UA node {address} failed")
  - Write template:
        node = client.get_node('{address}')
        if '{data_type}' == 'Float':
            variant = ua.Variant(float({value}), ua.VariantType.Float)
        else:
            variant = ua.Variant(int({value}), ua.VariantType.Int16)
        result = await node.write_value(variant)
  - Address format: NodeId, e.g. ns=2;i=1001
  - Notes: build a Variant with the type-specific VariantType.

Target protocol template: Modbus TCP
  - Port: 502
  - Library: pymodbus
  - Imports:
        from pymodbus.client import ModbusTcpClient
        import struct
        import time
  - Client init:   ModbusTcpClient(host='{host}', port={port})
  - Connect:       client.connect()
  - Disconnect:    client.close()
  - Read template:
        address_offset = {address} - 40001
        result = client.read_holding_registers(
            address=address_offset,
            count=2 if '{data_type}' == 'FLOAT32' else 1,
            slave=1)
        ...
  - Write template:
        address_offset = {address} - 40001
        if '{data_type}' == 'FLOAT32':
            high, low = struct.unpack('>HH',
                                      struct.pack('>f', float({value})))
            result = client.write_registers(address=address_offset,
                                            values=[high, low], slave=1)
        else:
            result = client.write_register(address=address_offset,
                                           value=int({value}), slave=1)
  - Address format: 40001-style; subtract 40001 to obtain the register.
  - Notes: FLOAT32 occupies 2 consecutive registers; use struct.

[L_map] -----------------------------------------------------------------
Address mappings (JSON, extracted from AddressMapping nodes):
[
  {
    "semantic_name": "temperature_sensor_01",
    "description":   "temperature sensor",
    "data_type":     "FLOAT32",
    "unit":          "C",
    "source":        "ns=2;i=1001",
    "target":        "40001"
  },
  {
    "semantic_name": "pressure_sensor_01",
    "description":   "pressure sensor",
    "data_type":     "FLOAT32",
    "unit":          "kPa",
    "source":        "ns=2;i=1002",
    "target":        "40004"
  },
  {
    "semantic_name": "valve_control_01",
    "description":   "valve opening",
    "data_type":     "UINT16",
    "unit":          "%",
    "source":        "ns=2;i=1003",
    "target":        "40003"
  }
]

[L_ops] -----------------------------------------------------------------
Required structure of the generated Python script:
  1. Imports:        union of the two protocol import blocks above.
  2. Server config:  OPC UA at localhost:4840; Modbus TCP at localhost:502.
  3. Client setup:   use the Client init templates above.
  4. Connections:    use the Connect / Disconnect code above.
  5. Core loop (continuous polling-with-write):
        - for each mapping item, await the async OPC UA read;
        - call the sync Modbus write directly (no await);
        - sleep between rounds; log every read/write;
        - catch and log errors per item; do not abort the loop.
  6. main():         full async main() with error handling and logging.
  7. Entry point:    if __name__ == "__main__": asyncio.run(main())

Adaptation guidance: mixed-mode (async source + sync target) - see above.
Protocol-specific hints: OPC UA VariantType per data_type; Modbus
    FLOAT32 occupies 2 consecutive registers (use struct).
General: follow the chosen architecture strictly; use the templates
    above as ground truth; log every conversion step.

[FA Constraints -- appended when function enhancement is enabled] ------
CRITICAL: strictly follow the provided templates. Do NOT substitute
API calls from training knowledge.
  pymodbus 3.x: count MUST be a keyword argument.
      correct: client.read_holding_registers(address, count=N, slave=1)
      wrong:   client.read_holding_registers(address, N, slave=1)
Copy the read/write template structure verbatim; only substitute the
{address}, {value}, {data_type} placeholders; preserve struct operations
and error handling as shown.
```
