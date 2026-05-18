#!/usr/bin/env python3
"""Build the translated IPC-CG prompt set from JSON templates.

Run from the repository root:
    python scripts/build_prompts.py
"""
from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str):
    with (ROOT / path).open(encoding="utf-8") as f:
        return json.load(f)


def mode_for(protocols, name: str) -> str:
    return protocols[name]["native_mode"]


def selected(protocols, name: str) -> dict:
    mode = mode_for(protocols, name)
    p = protocols[name]
    return {
        "mode": mode,
        "library": p["library"][mode],
        "imports": p["imports"][mode],
        "client_init": p["client_init"][mode],
        "connect": p["connect"][mode],
        "disconnect": p["disconnect"][mode],
        "read_template": p["read_template"][mode],
        "write_template": p["write_template"][mode],
    }


def indent_block(text: str, n: int = 8) -> str:
    pad = " " * n
    return "\n".join(pad + line if line else pad for line in str(text).splitlines())


def strip_prompt_margin(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        if line.startswith("    "):
            cleaned.append(line[4:])
        else:
            cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


def architecture_guidance(protocols, source: str, target: str) -> str:
    sm, tm = mode_for(protocols, source), mode_for(protocols, target)
    if sm == "async" and tm == "sync":
        return "mixed mode: async source + sync target; use async def main(), await source reads/messages, and call target synchronous writes directly in controlled blocks."
    if sm == "sync" and tm == "async":
        return "mixed mode: sync source + async target; use async def main(), execute source polling carefully, and await target writes."
    if sm == "async" and tm == "async":
        return "fully async mode; use a single event loop and await both source-side reads/messages and target-side writes."
    return "fully sync mode; use a simple polling loop with synchronous source reads and target writes."


def mapping_for(protocols, mappings, source: str, target: str) -> list[dict]:
    target_type_map = protocols[target].get("type_mapping", {})
    out = []
    for m in mappings:
        if source in m["addresses"] and target in m["addresses"]:
            out.append({
                "semantic_name": m["semantic_name"],
                "description": m["description"],
                "data_type": target_type_map.get(m["data_type"], m["data_type"]),
                "unit": m["unit"],
                "source": m["addresses"][source],
                "target": m["addresses"][target],
                "json_path": "",
                "array_length": 1,
                "element_type": "",
            })
    return out


def fa_constraints() -> str:
    return dedent("""
    [FA Constraints -- appended when function enhancement is enabled] ------
    CRITICAL: strictly follow the provided templates. Do NOT substitute API calls from training knowledge.
      pymodbus 3.x: count MUST be a keyword argument.
          correct: client.read_holding_registers(address=address_offset, count=N, slave=1)
          wrong:   client.read_holding_registers(address_offset, N, slave=1)
    Copy the read/write template structure; only substitute the {address}, {value}, {data_type}, and protocol-specific placeholders.
    Preserve struct operations, address-offset calculations, and error handling as shown.
    """).strip()


def render_prompt(protocols, mappings, source: str, target: str) -> str:
    sp, tp = protocols[source], protocols[target]
    ss, ts = selected(protocols, source), selected(protocols, target)
    maps = mapping_for(protocols, mappings, source, target)
    prompt = dedent(f"""
    You are an industrial protocol expert. Based on the complete protocol template information below, generate a standalone protocol conversion script.

    [L_arch] ----------------------------------------------------------------
    Conversion direction: {source} -> {target}
    Architecture: optimal ({architecture_guidance(protocols, source, target)})

    IMPORTANT: this is a UNIDIRECTIONAL converter ({source} -> {target}).
      - read only from {source};
      - write only to {target};
      - do NOT subscribe to or poll {target} as a source;
      - do NOT implement the reverse flow.

    [L_api] -----------------------------------------------------------------
    Source protocol template: {source}
      - Port: {sp['port']}
      - Library: {ss['library']}
      - Imports:
{indent_block(ss['imports'])}
      - Client init: {ss['client_init']}
      - Connect: {ss['connect']}
      - Disconnect: {ss['disconnect']}
      - Read template:
{indent_block(ss['read_template'])}
      - Write template:
{indent_block(ss['write_template'])}
      - Address format: {sp['address_format']}
      - Notes: {sp['special_notes']}

    Target protocol template: {target}
      - Port: {tp['port']}
      - Library: {ts['library']}
      - Imports:
{indent_block(ts['imports'])}
      - Client init: {ts['client_init']}
      - Connect: {ts['connect']}
      - Disconnect: {ts['disconnect']}
      - Read template:
{indent_block(ts['read_template'])}
      - Write template:
{indent_block(ts['write_template'])}
      - Address format: {tp['address_format']}
      - Notes: {tp['special_notes']}

    [L_map] -----------------------------------------------------------------
    Address mappings (JSON, extracted from AddressMapping nodes):
    {json.dumps(maps, indent=2, ensure_ascii=False)}

    [L_ops] -----------------------------------------------------------------
    Required structure of the generated Python script:
      1. Imports: union of the two protocol import blocks above.
      2. Server config: {source} at localhost:{sp['port']}; {target} at localhost:{tp['port']}.
      3. Client setup: use the Client init templates above.
      4. Connections: use the Connect / Disconnect code above.
      5. Core loop: follow the selected architecture; convert each mapping item from source to target; log every read/write; catch and log errors per item.
      6. main(): include complete error handling and cleanup.
      7. Entry point: include a directly runnable Python entry point.

    Adaptation guidance: {architecture_guidance(protocols, source, target)}
    Protocol-specific hints: source notes and target notes above are ground truth.
    General: follow the chosen architecture strictly; use the templates above as ground truth; log every conversion step.

    {fa_constraints()}
    """)
    return strip_prompt_margin(prompt)


def main() -> None:
    protocols = load_json("data/protocol_templates.json")
    mappings = load_json("data/address_mappings.json")
    directions = load_json("data/core_directions.json")
    out_dir = ROOT / "prompts" / "core_directions"
    out_dir.mkdir(parents=True, exist_ok=True)
    for d in directions:
        source, target = d["source"], d["target"]
        name = f"{source.lower().replace(' ', '_')}_to_{target.lower().replace(' ', '_')}.md"
        content = f"# Prompt: {source} -> {target}\n\nInteraction class: {d['interaction']}\n\n```text\n{render_prompt(protocols, mappings, source, target)}```\n"
        (out_dir / name).write_text(content, encoding="utf-8")
    print(f"Wrote {len(directions)} prompts to {out_dir}")


if __name__ == "__main__":
    main()
