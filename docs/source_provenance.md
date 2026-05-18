# Source Provenance

This folder provides the public prompt artifacts associated with the IPC-CG manuscript.

Relevant source materials:

- Appendix B of the manuscript contains the representative OPC UA -> Modbus TCP prompt excerpt.
- Protocol-template and address-mapping fields are normalized into `data/protocol_templates.json` and `data/address_mappings.json`.
- The 12 core directions are listed in `data/core_directions.json` and reproduced as prompt files under `prompts/core_directions/`.

Excluded from this public package:

- API configuration files.
- Neo4j database credentials.
- Private generated artifacts, logs, `.pid` files, and manuscript-review internal drafts.
