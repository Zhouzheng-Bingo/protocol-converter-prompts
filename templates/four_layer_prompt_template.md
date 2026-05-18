# Four-Layer Structured Prompt Template

```text
You are an industrial protocol expert. Based on the complete protocol template information below, generate a standalone protocol conversion script.

[L_arch] ----------------------------------------------------------------
Conversion direction: {source_protocol} -> {target_protocol}
Architecture: {architecture_mode} ({architecture_guidance})

IMPORTANT: this is a UNIDIRECTIONAL converter ({source_protocol} -> {target_protocol}).
  - read only from {source_protocol};
  - write only to {target_protocol};
  - do NOT subscribe to or poll {target_protocol} as a source;
  - do NOT implement the reverse flow.

[L_api] -----------------------------------------------------------------
Source protocol template: {source_protocol}
  - Port: {source_port}
  - Library: {source_library}
  - Imports: {source_imports}
  - Client init: {source_client_init}
  - Connect: {source_connect}
  - Disconnect: {source_disconnect}
  - Read template: {source_read_template}
  - Write template: {source_write_template}
  - Address format: {source_address_format}
  - Notes: {source_notes}

Target protocol template: {target_protocol}
  - Port: {target_port}
  - Library: {target_library}
  - Imports: {target_imports}
  - Client init: {target_client_init}
  - Connect: {target_connect}
  - Disconnect: {target_disconnect}
  - Read template: {target_read_template}
  - Write template: {target_write_template}
  - Address format: {target_address_format}
  - Notes: {target_notes}

[L_map] -----------------------------------------------------------------
Address mappings (JSON, extracted from AddressMapping nodes):
{address_mappings_json}

[L_ops] -----------------------------------------------------------------
Required structure of the generated Python script:
  1. Imports: union of the two protocol import blocks above.
  2. Server config: source and target endpoints.
  3. Client setup: use the Client init templates above.
  4. Connections: use the Connect / Disconnect code above.
  5. Core loop: follow the selected architecture and mapping list.
  6. main(): include complete error handling and cleanup.
  7. Entry point: include a directly runnable Python entry point.

[FA Constraints -- optional] --------------------------------------------
{function_enhancement_constraints}
```
