# Function-Enhancement Constraints

```text
[FA Constraints -- appended when function enhancement is enabled] ------
CRITICAL: strictly follow the provided templates. Do NOT substitute API calls from training knowledge.
  pymodbus 3.x: count MUST be a keyword argument.
      correct: client.read_holding_registers(address=address_offset, count=N, slave=1)
      wrong:   client.read_holding_registers(address_offset, N, slave=1)
Copy the read/write template structure; only substitute the {address}, {value}, {data_type}, and protocol-specific placeholders.
Preserve struct operations, address-offset calculations, and error handling as shown.

Structured payload handling, when mapping entries carry json_path / array_length / element_type:
  - extract values via the declared path;
  - process all mappings sharing the same source topic or endpoint;
  - use array_length to choose scalar versus array writes;
  - preserve the target protocol register or payload footprint.
```
