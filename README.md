# Protocol Converter Prompts

This repository contains the translated structured prompt artifacts for the IPC-CG framework described in the manuscript **"Harnessing LLMs for Industrial Protocol Conversion Code Generation with Knowledge Graphs and Function Enhancement"**.

The prompt format follows the four-layer structure used in the paper:

- `L_arch`: conversion direction and architecture constraints.
- `L_api`: protocol interface templates, imports, client setup, read/write primitives, and protocol-specific notes.
- `L_map`: address mappings extracted from `AddressMapping` entries.
- `L_ops`: operational requirements for the generated standalone Python converter.
- `FA Constraints`: function-enhancement constraints used to prevent API drift and enforce executable primitives.

## Contents

- `prompts/appendix_b_opcua_to_modbus_tcp.md`: representative prompt excerpt corresponding to Appendix B of the manuscript.
- `prompts/core_directions/`: translated prompts for the 12 representative protocol-conversion directions used in the core task set.
- `templates/four_layer_prompt_template.md`: generic four-layer prompt template.
- `templates/fa_constraints.md`: function-enhancement constraint block.
- `data/protocol_templates.json`: public protocol-template fields used to assemble the prompts.
- `data/address_mappings.json`: representative semantic address mappings used in the prompt examples.
- `data/core_directions.json`: the 12 representative conversion directions.
- `scripts/build_prompts.py`: reproducible prompt-generation script.

## Regenerate Prompt Files

```bash
python scripts/build_prompts.py
```

The script has no external Python dependencies.

## Scope Note

These files are prompt artifacts for transparency and reproducibility. They do not include API keys, database credentials, private LLM invocation logs, or generated converter outputs.
