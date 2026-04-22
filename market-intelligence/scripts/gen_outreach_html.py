#!/usr/bin/env python3
"""
gen_outreach_html.py — Market Intelligence Skill
Generates a searchable, filterable dark-theme HTML outreach tool from vault People notes.

Usage:
  python3 gen_outreach_html.py \
    --vault-path /path/to/vault \
    --output /path/to/outreach.html \
    --title "Outreach: My Campaign" \
    [--filter-tags "founder,investor"] \
    [--filter-priority "critical,high"] \
    [--sections "Infrastructure Founders,Investors"]

Or pass contacts directly as a Python list of dicts — see CONTACT_SCHEMA at the bottom.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


# ─── Frontmatter parser ───────────────────────────────────────────────────────

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from a markdown file. Returns (meta, body)."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    front = content[3:end].strip()
    body = content[end + 4:].strip()
    if yaml:
        try:
            return yaml.safe_load(front) or {}, body
        except Exception:
            pass
    # Fallback: minimal key:value parser
    meta = {}
    for line in front.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"')
    return meta, body


# ─── Vault reader ─────────────────────────────────────────────────────────────

def load_contacts_from_vault(
    vault_path: str,
    filter_tags: list[str] | None = None,
    filter_priority: list[str] | None = None,
    sections: list[str] | None = None,
) -> list[dict]:
    """
    Reads all Person notes from {vault_path}/Market Landscape/People/
    and returns a list of contact dicts.
    """
    people_dir = Path(vault_path) / "Market Landscape" / "People"
    if not people_dir.exists():
        print(f"Warning: People directory not found at {people_dir}", file=sys.stderr)
        return []

    contacts = []
    for md_file in sorted(people_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        if not meta:
            continue

        # Extract fields
        tags = meta.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        priority = meta.get("priority") or ""
        outreach_tier = meta.get("outreach_tier") or ""
        fit_score = meta.get("fit_score") or ""

        # Apply filters
        if filter_tags and not any(t in tags for t in filter_tags):
            continue
        if filter_priority and priority not in filter_priority:
            continue

        # Extract outreach angle from body
        angle = ""
        angle_match = re.search(r"## Outreach angle\s*\n+>\s*(.+)", body, re.IGNORECASE)
        if angle_match:
            angle = angle_match.group(1).strip().strip('"')

        # Extract recent signal from body
        signal = ""
        signal_match = re.search(r"## Public signals?\s*\n+[-*]\s*(.+)", body, re.IGNORECASE)
        if signal_match:
            signal = signal_match.group(1).strip()

        # Determine section
        section = meta.get("section") or meta.get("category") or "Other"
        if sections and section not in sections:
            # Try matching on tags
            matched = False
            for s in (sections or []):
                if any(s.lower() in t.lower() for t in tags):
                    section = s
                    matched = True
                    break
            if not matched and sections:
                continue  # Skip if section filtering is strict

        company_raw = meta.get("company") or ""
        company = re.sub(r"\[\[|\]\]", "", company_raw)

        contact = {
            "name": meta.get("name") or md_file.stem,
            "role": meta.get("role") or "",
            "company": company,
            "section": section,
            "handles": {
                "twitter": meta.get("twitter") or "",
                "twitter_url": meta.get("twitter_url") or (
                    f"https://x.com/{meta['twitter'].lstrip('@')}" if meta.get("twitter") else ""
                ),
                "linkedin": meta.get("linkedin") or "",
                "github": meta.get("github") or "",
                "email": meta.get("email") or "",
            },
            "scoring": {
                "tier": outreach_tier,
                "priority": priority,
                "fit_score": fit_score,
            },
            "outreach": {
                "angle": angle,
                "signal": signal,
                "type": "cold-dm",
            },
            "verification": {
                "handle_verified": bool(meta.get("handle_verified")),
                "verified_date": meta.get("handle_verified_date") or "",
                "verified_method": meta.get("handle_verified_method") or "",
            },
            "tags": tags,
        }
        contacts.append(contact)

    return contacts


# ─── HTML generator ──────────────────────────────────────────────────────────

TIER_COLORS = {
    "A": ("#f85149", "critical"),
    "B": ("#f0883e", "high"),
    "C": ("#d29922", "medium"),
    "D": ("#6e7681", "low"),
    "critical": ("#f85149", "critical"),
    "high": ("#f0883e", "high"),
    "medium": ("#d29922", "medium"),
    "low": ("#6e7681", "low"),
}


def tier_badge(tier: str) -> str:
    color, label = TIER_COLORS.get(tier, ("#6e7681", tier or "?"))
    display = tier.upper() if len(tier) == 1 else tier.capitalize()
    return f'<span class="badge" style="background:{color}">{display}</span>'


def verified_badge(verified: bool) -> str:
    if verified:
        return '<span class="badge verified">✓ Verified</span>'
    return '<span class="badge unverified">⚠ Unverified</span>'


def render_card(contact: dict) -> str:
    handles = contact.get("handles", {})
    scoring = contact.get("scoring", {})
    outreach = contact.get("outreach", {})
    verification = contact.get("verification", {})
    tags = contact.get("tags", [])

    twitter = handles.get("twitter", "")
    twitter_url = handles.get("twitter_url", "")
    linkedin = handles.get("linkedin", "")
    github = handles.get("github", "")

    tier = scoring.get("tier") or scoring.get("priority") or ""
    angle = outreach.get("angle", "")
    signal = outreach.get("signal", "")
    verified = verification.get("handle_verified", False)

    handle_display = twitter or linkedin or github or ""
    handle_url = twitter_url or linkedin or github or ""

    tag_html = " ".join(
        f'<span class="tag">{t}</span>' for t in tags[:6]
    )

    handle_block = ""
    if handle_display:
        handle_block = f'''
        <div class="handle-row">
          <span class="handle-label">Handle:</span>
          <span class="handle">
            {f'<a href="{handle_url}" target="_blank" class="handle-link">{handle_display}</a>' if handle_url else handle_display}
          </span>
          {f'<button class="copy-btn" data-copy="{handle_display}" title="Copy handle">📋</button>' if handle_display else ""}
        </div>'''

    platform_links = []
    if twitter_url:
        platform_links.append(f'<a href="{twitter_url}" target="_blank" class="platform-link">𝕏</a>')
    if linkedin:
        platform_links.append(f'<a href="{linkedin}" target="_blank" class="platform-link">in</a>')
    if github:
        platform_links.append(f'<a href="{github}" target="_blank" class="platform-link">⌥</a>')

    contact_name = contact.get("name", "")
    contact_role = contact.get("role", "")
    contact_company = contact.get("company", "")

    search_data = " ".join([
        contact_name, contact_role, contact_company,
        handle_display, angle, signal, " ".join(tags), tier
    ]).lower()

    opener_text = f"Hey {contact_name.split()[0]}, {angle}" if angle else ""

    return f'''
<div class="card" data-section="{contact.get('section','')}" data-tier="{tier}" data-search="{search_data}">
  <div class="card-header">
    <div class="card-left">
      {tier_badge(tier) if tier else ""}
      {verified_badge(verified)}
      <span class="contact-name">{contact_name}</span>
      <span class="contact-meta">{f"— {contact_role}" if contact_role else ""} {f"at {contact_company}" if contact_company else ""}</span>
    </div>
    <div class="platform-links">{" ".join(platform_links)}</div>
  </div>
  {f'<div class="tag-row">{tag_html}</div>' if tag_html else ""}
  {handle_block}
  {f'<div class="angle-row"><span class="field-label">Angle:</span> <span class="angle-text">{angle}</span>{f\'<button class="copy-btn" data-copy="{opener_text}" title="Copy opener">📝</button>\' if opener_text else ""}</div>' if angle else ""}
  {f'<div class="signal-row"><span class="field-label">Signal:</span> <span class="signal-text">{signal}</span></div>' if signal else ""}
</div>'''


def generate_html(
    contacts: list[dict],
    title: str = "Outreach List",
    generated_date: str = "",
) -> str:
    if not generated_date:
        generated_date = datetime.now().strftime("%B %d, %Y")

    # Group by section
    sections: dict[str, list[dict]] = {}
    for c in contacts:
        s = c.get("section") or "Other"
        sections.setdefault(s, []).append(c)

    # Tier distribution
    tier_counts: dict[str, int] = {}
    for c in contacts:
        t = c.get("scoring", {}).get("tier") or c.get("scoring", {}).get("priority") or "?"
        tier_counts[t] = tier_counts.get(t, 0) + 1

    tier_stats = " · ".join(
        f'<span style="color:{TIER_COLORS.get(t, ("#888",""))[0]}">{t}: {n}</span>'
        for t, n in sorted(tier_counts.items())
    )

    section_tabs = "\n".join(
        f'<button class="tab" data-section="{s}">{s} <span class="count">{len(cs)}</span></button>'
        for s, cs in sections.items()
    )

    all_cards = "\n".join(render_card(c) for c in contacts)

    contacts_json = json.dumps(contacts, indent=2, default=str)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  :root {{
    --bg: #0d1117; --bg2: #161b22; --bg3: #1c2128;
    --border: #30363d; --text: #e6edf3; --muted: #8b949e;
    --blue: #58a6ff; --green: #3fb950; --red: #f85149;
    --orange: #f0883e; --yellow: #d29922;
    --font-mono: 'SF Mono', 'Fira Code', monospace;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: -apple-system, system-ui, sans-serif; min-height: 100vh; }}
  a {{ color: var(--blue); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}

  /* Header */
  .header {{ background: var(--bg2); border-bottom: 1px solid var(--border); padding: 16px 24px; position: sticky; top: 0; z-index: 100; }}
  .header-row1 {{ display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }}
  .title {{ font-size: 18px; font-weight: 600; }}
  .meta {{ color: var(--muted); font-size: 13px; }}
  .stats {{ font-size: 12px; color: var(--muted); margin-bottom: 10px; }}

  /* Controls */
  .controls {{ display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }}
  .search-wrap {{ flex: 1; min-width: 200px; }}
  input[type=search] {{
    width: 100%; background: var(--bg3); border: 1px solid var(--border);
    border-radius: 6px; padding: 7px 12px; color: var(--text); font-size: 14px;
    outline: none;
  }}
  input[type=search]:focus {{ border-color: var(--blue); }}
  input[type=search]::placeholder {{ color: var(--muted); }}

  /* Tabs */
  .tabs {{ display: flex; gap: 4px; flex-wrap: wrap; }}
  .tab {{
    background: var(--bg3); border: 1px solid var(--border); border-radius: 6px;
    color: var(--muted); cursor: pointer; font-size: 12px; padding: 5px 10px;
    white-space: nowrap;
  }}
  .tab:hover, .tab.active {{ background: var(--bg2); border-color: var(--blue); color: var(--text); }}
  .tab .count {{ color: var(--muted); margin-left: 4px; }}

  /* Tier filter */
  .tier-filters {{ display: flex; gap: 4px; }}
  .tier-btn {{
    background: var(--bg3); border: 1px solid var(--border); border-radius: 6px;
    color: var(--muted); cursor: pointer; font-size: 12px; padding: 5px 8px;
  }}
  .tier-btn:hover {{ border-color: var(--blue); color: var(--text); }}
  .tier-btn.active {{ color: var(--text); border-color: currentColor; }}

  /* Main */
  .main {{ padding: 20px 24px; max-width: 1100px; margin: 0 auto; }}

  /* Section header */
  .section-label {{
    color: var(--muted); font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.8px; margin: 20px 0 8px; padding-bottom: 4px;
    border-bottom: 1px solid var(--border);
  }}

  /* Cards */
  .card {{
    background: var(--bg2); border: 1px solid var(--border); border-radius: 8px;
    padding: 14px 16px; margin-bottom: 8px; transition: border-color 0.15s;
  }}
  .card:hover {{ border-color: #444c56; }}
  .card.hidden {{ display: none; }}

  .card-header {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px; }}
  .card-left {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }}

  .badge {{
    border-radius: 4px; color: #fff; font-size: 11px; font-weight: 700;
    padding: 2px 7px; white-space: nowrap;
  }}
  .badge.verified {{ background: #1a3a2a; color: var(--green); border: 1px solid #2d6a4a; }}
  .badge.unverified {{ background: #3a2a1a; color: var(--orange); border: 1px solid #6a4a2d; }}

  .contact-name {{ font-weight: 600; font-size: 15px; }}
  .contact-meta {{ color: var(--muted); font-size: 13px; }}

  .platform-links {{ display: flex; gap: 6px; }}
  .platform-link {{
    background: var(--bg3); border: 1px solid var(--border); border-radius: 4px;
    color: var(--muted); font-size: 11px; font-weight: 600; padding: 2px 6px;
    text-decoration: none;
  }}
  .platform-link:hover {{ color: var(--text); border-color: #58a6ff; text-decoration: none; }}

  .tag-row {{ margin-bottom: 6px; display: flex; gap: 4px; flex-wrap: wrap; }}
  .tag {{
    background: var(--bg3); border: 1px solid var(--border); border-radius: 12px;
    color: var(--muted); font-size: 11px; padding: 2px 8px;
  }}

  .handle-row, .angle-row, .signal-row {{
    display: flex; align-items: flex-start; gap: 6px; margin-top: 4px; font-size: 13px;
  }}
  .field-label {{ color: var(--muted); white-space: nowrap; min-width: 50px; }}
  .handle {{ font-family: var(--font-mono); color: var(--blue); }}
  .handle-link {{ color: var(--blue); }}
  .angle-text {{ color: var(--text); flex: 1; }}
  .signal-text {{ color: var(--muted); font-size: 12px; flex: 1; }}

  .copy-btn {{
    background: none; border: 1px solid var(--border); border-radius: 4px;
    color: var(--muted); cursor: pointer; font-size: 11px; padding: 1px 5px;
    white-space: nowrap;
  }}
  .copy-btn:hover {{ color: var(--text); border-color: var(--blue); }}
  .copy-btn.copied {{ color: var(--green); border-color: var(--green); }}

  .no-results {{ color: var(--muted); padding: 40px; text-align: center; font-size: 14px; }}
</style>
</head>
<body>

<div class="header">
  <div class="header-row1">
    <div class="title">{title}</div>
    <div class="meta">{len(contacts)} contacts · {generated_date}</div>
  </div>
  <div class="stats">{tier_stats}</div>
  <div class="controls">
    <div class="search-wrap">
      <input type="search" id="search" placeholder="Search by name, company, role, tag, or angle…" autofocus>
    </div>
    <div class="tier-filters" id="tier-filters">
      <button class="tier-btn active" data-tier="all">All</button>
      <button class="tier-btn" data-tier="A" style="color:#f85149">A</button>
      <button class="tier-btn" data-tier="B" style="color:#f0883e">B</button>
      <button class="tier-btn" data-tier="C" style="color:#d29922">C</button>
      <button class="tier-btn" data-tier="D" style="color:#6e7681">D</button>
      <button class="tier-btn" data-tier="critical" style="color:#f85149">Critical</button>
      <button class="tier-btn" data-tier="high" style="color:#f0883e">High</button>
    </div>
  </div>
  <div class="tabs" id="tabs" style="margin-top:8px">
    <button class="tab active" data-section="all">All <span class="count">{len(contacts)}</span></button>
    {section_tabs}
  </div>
</div>

<div class="main" id="main">
  {all_cards}
  <div class="no-results hidden" id="no-results">No contacts match your search.</div>
</div>

<script>
const contacts = {contacts_json};

// State
let activeSection = 'all';
let activeTier = 'all';
let searchQuery = '';

function updateVisible() {{
  const cards = document.querySelectorAll('.card');
  let visible = 0;

  // Group rendering: show section labels only if section has visible cards
  const sectionCounts = {{}};

  cards.forEach(card => {{
    const section = card.dataset.section || '';
    const tier = (card.dataset.tier || '').toLowerCase();
    const search = card.dataset.search || '';

    const sectionMatch = activeSection === 'all' || section === activeSection;
    const tierMatch = activeTier === 'all' || tier === activeTier.toLowerCase();
    const searchMatch = !searchQuery || search.includes(searchQuery.toLowerCase());

    const show = sectionMatch && tierMatch && searchMatch;
    card.classList.toggle('hidden', !show);
    if (show) {{
      visible++;
      sectionCounts[section] = (sectionCounts[section] || 0) + 1;
    }}
  }});

  // Show/hide section labels
  document.querySelectorAll('.section-label').forEach(label => {{
    const s = label.dataset.section;
    label.style.display = (sectionCounts[s] || 0) > 0 ? '' : 'none';
  }});

  document.getElementById('no-results').classList.toggle('hidden', visible > 0);
}}

// Search
document.getElementById('search').addEventListener('input', e => {{
  searchQuery = e.target.value.trim();
  updateVisible();
}});

// Tabs
document.getElementById('tabs').addEventListener('click', e => {{
  const btn = e.target.closest('.tab');
  if (!btn) return;
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  activeSection = btn.dataset.section;
  updateVisible();
}});

// Tier filter
document.getElementById('tier-filters').addEventListener('click', e => {{
  const btn = e.target.closest('.tier-btn');
  if (!btn) return;
  document.querySelectorAll('.tier-btn').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  activeTier = btn.dataset.tier;
  updateVisible();
}});

// Copy buttons
document.addEventListener('click', e => {{
  const btn = e.target.closest('.copy-btn');
  if (!btn) return;
  const text = btn.dataset.copy;
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {{
    btn.classList.add('copied');
    const orig = btn.textContent;
    btn.textContent = '✓';
    setTimeout(() => {{ btn.classList.remove('copied'); btn.textContent = orig; }}, 1500);
  }});
}});

// Add section labels between sections
(function() {{
  const main = document.getElementById('main');
  const cards = [...main.querySelectorAll('.card')];
  let lastSection = null;
  cards.forEach(card => {{
    const s = card.dataset.section;
    if (s && s !== lastSection) {{
      const label = document.createElement('div');
      label.className = 'section-label';
      label.dataset.section = s;
      label.textContent = s;
      main.insertBefore(label, card);
      lastSection = s;
    }}
  }});
}})();

updateVisible();
</script>
</body>
</html>"""


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate outreach HTML from vault notes")
    parser.add_argument("--vault-path", required=True, help="Path to the Obsidian vault root")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument("--title", default="Outreach List", help="Page title")
    parser.add_argument("--filter-tags", help="Comma-separated tags to include")
    parser.add_argument("--filter-priority", help="Comma-separated priorities to include")
    parser.add_argument("--sections", help="Comma-separated section names to include")
    args = parser.parse_args()

    filter_tags = [t.strip() for t in args.filter_tags.split(",")] if args.filter_tags else None
    filter_priority = [p.strip() for p in args.filter_priority.split(",")] if args.filter_priority else None
    sections = [s.strip() for s in args.sections.split(",")] if args.sections else None

    contacts = load_contacts_from_vault(
        args.vault_path,
        filter_tags=filter_tags,
        filter_priority=filter_priority,
        sections=sections,
    )

    if not contacts:
        print(f"No contacts found matching criteria in {args.vault_path}", file=sys.stderr)
        sys.exit(1)

    html = generate_html(contacts, title=args.title)
    Path(args.output).write_text(html, encoding="utf-8")
    print(f"Wrote: {args.output}")
    print(f"Total contacts: {len(contacts)}")


# ─── Direct use: pass contacts as a list of dicts ────────────────────────────
# CONTACT_SCHEMA (minimum required fields):
# {
#   "name": str,
#   "role": str,
#   "company": str,
#   "section": str,                          # display group label
#   "handles": {"twitter": "@x", "twitter_url": "...", "linkedin": "...", "github": "..."},
#   "scoring": {"tier": "A|B|C|D", "priority": "critical|high|medium|low"},
#   "outreach": {"angle": "...", "signal": "..."},
#   "verification": {"handle_verified": bool},
#   "tags": ["tag1", "tag2"],
# }

if __name__ == "__main__":
    main()
