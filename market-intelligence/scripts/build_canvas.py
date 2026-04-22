#!/usr/bin/env python3
"""
build_canvas.py — Market Intelligence Canvas Generator

Reads all vault notes and generates a landscape.canvas JSON file
following the Obsidian JSON Canvas 1.0 spec.

Usage:
    python build_canvas.py <vault-root> [--output landscape.canvas]

The script:
1. Scans all notes in Market Landscape/{Prospects,Competitors,People,ICPs}
2. Groups prospects by category frontmatter
3. Lays out nodes spatially (Competitors left, Product center, Prospects right)
4. Assigns colors by priority/tier
5. Generates edges: companies → investors, founders → companies
6. Validates all file paths before writing

Configuration: Edit the LAYOUT and COLOR constants below for your domain.
"""

import json
import os
import sys
import re
import random
import string
from pathlib import Path

# ─── Layout constants ──────────────────────────────────────────────────────
CANVAS_LAYOUT = {
    "competitor_x": -2400,
    "product_x": -200,
    "prospect_x_start": 500,
    "prospect_x_step": 900,       # horizontal distance between segment columns
    "group_y_start": -2000,       # topmost group y position
    "group_y_step": 700,          # vertical distance between segment groups
    "node_width": 260,
    "node_height": 60,
    "group_padding": 60,
    "market_signal_x": -1400,
    "icp_x": 150,
}

# Node colors (Obsidian 1–6: red, orange, yellow, green, cyan, purple)
PRIORITY_COLORS = {
    "critical": "1",   # red
    "high": "2",       # orange
    "medium": "3",     # yellow
    "low": "4",        # green
}
TIER_COLORS = {
    "1": "1",          # red
    "1.5": "2",        # orange
    "2": "3",          # yellow
    "T1": "1", "T2": "3", "T3": "4",
    "3": "4",          # green
}
PERSON_COLOR = "5"     # cyan
ICP_COLOR = "6"        # purple
PRODUCT_COLOR = "6"    # purple

# ─── Helpers ──────────────────────────────────────────────────────────────

def make_id(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm_text = text[4:end]
    result = {}
    for line in fm_text.splitlines():
        m = re.match(r'^(\w[\w_-]*):\s*(.*)', line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            result[key] = val if val and val != "null" else None
    return result

def file_node(node_id, file_path_rel, x, y, w, h, color=None):
    n = {"id": node_id, "type": "file", "file": file_path_rel,
         "x": x, "y": y, "width": w, "height": h}
    if color:
        n["color"] = color
    return n

def text_node(node_id, text, x, y, w, h, color=None):
    n = {"id": node_id, "type": "text", "text": text,
         "x": x, "y": y, "width": w, "height": h}
    if color:
        n["color"] = color
    return n

def edge(from_id, to_id, label=None, from_side="right", to_side="left"):
    e = {"id": make_id(), "fromNode": from_id, "fromSide": from_side,
         "toNode": to_id, "toSide": to_side}
    if label:
        e["label"] = label
    return e

# ─── Main ─────────────────────────────────────────────────────────────────

def build_canvas(vault_root: str, output_path: str = None):
    vault = Path(vault_root)
    ml = vault / "Market Landscape"

    if not ml.exists():
        print(f"ERROR: Market Landscape/ not found at {ml}", file=sys.stderr)
        sys.exit(1)

    nodes = []
    edges = []
    node_map = {}  # filename stem → node_id (for edge generation)

    L = CANVAS_LAYOUT
    NW, NH = L["node_width"], L["node_height"]

    # ── 1. Product / center node ──────────────────────────────────────────
    product_node_id = make_id()
    product_name = vault.name.replace("-", " ").title()  # infer from vault folder name
    nodes.append(text_node(product_node_id, f"**{product_name}**\n_Your Product_",
                           L["product_x"], 0, 300, 80, PRODUCT_COLOR))

    # ── 2. Competitors ────────────────────────────────────────────────────
    comp_dir = ml / "Competitors"
    if comp_dir.exists():
        comp_files = sorted(comp_dir.glob("*.md"))
        comp_y_start = -(len(comp_files) * (NH + 20)) // 2
        for i, cf in enumerate(comp_files):
            fm = parse_frontmatter(cf)
            tier = fm.get("tier", "3")
            color = TIER_COLORS.get(str(tier), "4")
            rel = str(cf.relative_to(vault))
            nid = make_id()
            x = L["competitor_x"] + (i % 2) * (NW + 20)
            y = comp_y_start + (i // 2) * (NH + 20)
            nodes.append(file_node(nid, rel, x, y, NW, NH, color))
            node_map[cf.stem] = nid

    # ── 3. Prospects — grouped by category ───────────────────────────────
    prospect_dir = ml / "Prospects"
    if prospect_dir.exists():
        prospect_files = sorted(prospect_dir.glob("*.md"))
        # Group by category
        groups = {}
        for pf in prospect_files:
            fm = parse_frontmatter(pf)
            cat = fm.get("category") or "uncategorized"
            groups.setdefault(cat, []).append((pf, fm))

        # Sort groups: higher-priority groups first
        def group_priority(items):
            scores = {"critical": 0, "high": 1, "medium": 2, "low": 3, None: 4}
            return min(scores.get(fm.get("priority"), 4) for _, fm in items)

        sorted_groups = sorted(groups.items(), key=lambda kv: group_priority(kv[1]))

        col = 0  # column index for prospect groups
        for cat, items in sorted_groups:
            x_base = L["prospect_x_start"] + col * L["prospect_x_step"]
            y_base = L["group_y_start"]

            # Group background node
            group_h = len(items) * (NH + 15) + L["group_padding"] * 2
            group_w = NW + L["group_padding"] * 2
            group_id = make_id()
            group_label = cat.replace("-", " ").title()
            nodes.append(text_node(group_id, group_label,
                                   x_base - L["group_padding"],
                                   y_base - L["group_padding"],
                                   group_w, group_h, "3"))

            for j, (pf, fm) in enumerate(items):
                priority = fm.get("priority", "low")
                color = PRIORITY_COLORS.get(priority, "4")
                rel = str(pf.relative_to(vault))
                nid = make_id()
                x = x_base
                y = y_base + j * (NH + 15)
                nodes.append(file_node(nid, rel, x, y, NW, NH, color))
                node_map[pf.stem] = nid

                # Edge: prospect → product center (if critical/high)
                if priority in ("critical", "high"):
                    edges.append(edge(nid, product_node_id, from_side="left", to_side="right"))

            col += 1

    # ── 4. People ─────────────────────────────────────────────────────────
    people_dir = ml / "People"
    if people_dir.exists():
        people_files = sorted(people_dir.glob("*.md"))
        # Place people in a column to the right of the rightmost prospects
        px_base = L["prospect_x_start"] + (col + 1) * L["prospect_x_step"] if 'col' in dir() else L["prospect_x_start"] + L["prospect_x_step"]
        py_base = -600
        for i, pf in enumerate(people_files):
            fm = parse_frontmatter(pf)
            rel = str(pf.relative_to(vault))
            nid = make_id()
            x = px_base + (i % 2) * (NW + 20)
            y = py_base + (i // 2) * (NH + 20)
            nodes.append(file_node(nid, rel, x, y, NW, NH, PERSON_COLOR))
            node_map[pf.stem] = nid

            # Edge: person → their company (if company note exists)
            company = fm.get("company")
            if company:
                company_clean = company.replace("[[", "").replace("]]", "")
                if company_clean in node_map:
                    edges.append(edge(nid, node_map[company_clean], "works at"))

    # ── 5. ICPs ───────────────────────────────────────────────────────────
    icp_dir = ml / "ICPs"
    if icp_dir.exists():
        icp_files = sorted(icp_dir.glob("*.md"))
        for i, icp in enumerate(icp_files):
            rel = str(icp.relative_to(vault))
            nid = make_id()
            nodes.append(file_node(nid, rel, L["icp_x"], -300 + i * (NH + 20), NW, NH, ICP_COLOR))
            edges.append(edge(product_node_id, nid, "serves", from_side="right", to_side="left"))

    # ── 6. Market signals card ────────────────────────────────────────────
    index_path = vault / "Market Landscape" / "_Index.md"
    if index_path.exists():
        signals_id = make_id()
        nodes.append(text_node(signals_id, "**📡 Market Signals**\n_See _Index.md for full breakdown_",
                               L["market_signal_x"], -200, 360, 80, "5"))
        edges.append(edge(signals_id, product_node_id))

    # ── 7. Validate all file nodes ────────────────────────────────────────
    errors = []
    for n in nodes:
        if n.get("type") == "file":
            full = vault / n["file"]
            if not full.exists():
                errors.append(n["file"])

    if errors:
        print(f"WARNING: {len(errors)} file nodes point to non-existent files:", file=sys.stderr)
        for e_path in errors[:10]:
            print(f"  ✗ {e_path}", file=sys.stderr)
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more", file=sys.stderr)

    # ── 8. Write canvas ───────────────────────────────────────────────────
    canvas_data = {"nodes": nodes, "edges": edges}
    out = output_path or str(vault / "landscape.canvas")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(canvas_data, f, indent=2, ensure_ascii=False)

    valid_nodes = len([n for n in nodes if n.get("type") == "file" and (vault / n["file"]).exists()])
    print(f"✅ Canvas written: {out}")
    print(f"   {len(nodes)} nodes ({valid_nodes} valid file nodes, {len(nodes) - valid_nodes} text/group)")
    print(f"   {len(edges)} edges")
    if errors:
        print(f"   ⚠️  {len(errors)} broken file references (see warnings above)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_canvas.py <vault-root> [--output landscape.canvas]")
        sys.exit(1)

    vault_root = sys.argv[1]
    output = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output = sys.argv[idx + 1]

    build_canvas(vault_root, output)
