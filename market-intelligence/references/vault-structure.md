# Vault Structure Reference

Complete specification for the market intelligence vault layout, naming conventions, canvas design, and Obsidian Bases setup.

---

## Folder layout

```
{vault-root}/
├── Market Landscape/
│   ├── Prospects/
│   │   └── [Company Name].md      # One note per target company
│   ├── Competitors/
│   │   └── [Company Name].md      # One note per competitor
│   ├── People/
│   │   └── [Full Name].md         # One note per person
│   ├── Investors/
│   │   └── [Firm Name].md         # One note per VC firm
│   ├── ICPs/
│   │   └── T1-[ICP-Name].md       # Prefixed by tier for sort order
│   └── Intel/
│       └── [Topic Name].md        # Free-form research notes
├── _Index.md                       # Master index — always up to date
├── landscape.canvas                # Visual map — rebuild after major additions
├── Prospects DB.base               # Database view over Prospects/
├── Competitors DB.base             # Database view over Competitors/
├── People DB.base                  # Database view over People/
└── Market Intelligence.base        # Master cross-collection view
```

---

## Naming conventions

### Files
- **Company notes**: Exact company name as displayed publicly. `Lindy AI.md`, `Browserbase.md`, `1Password UA.md`
- **Person notes**: Full name. `Flo Crivello.md`, `Andrew Lee.md`
- **ICP notes**: `T1-AI-Agent-Platform-Builder.md` — tier prefix for sort order
- **Intel notes**: Descriptive, date-free. `Integration Map.md`, `Investor Map.md`

### Naming rules
- No trailing spaces or special characters except hyphens and periods
- Title case for company and person names
- Kebab-case for ICP filenames after the tier prefix
- Never include dates in filenames — use frontmatter `last_researched` instead

---

## _Index.md structure

The index is the entry point to the vault. Keep it scannable. Update it whenever 5+ entities are added.

```markdown
---
last_updated: "YYYY-MM-DD"
total_prospects: XX
total_competitors: XX
total_people: XX
---

# Market Intelligence — [Domain Name]

> [One sentence describing what this landscape covers and for what product/company.]

## Market signals
- [Key stat or trend #1 — with source]
- [Key stat or trend #2]
- [Key stat or trend #3]

## Prospects by priority

### 🔴 Critical
- [[Company A]] — [one-line why]
- [[Company B]] — [one-line why]

### 🟠 High
- [[Company C]]
- [[Company D]]

## Competitors by tier

### Tier 1 — Direct threats
- [[Competitor A]] — [one-line differentiation]

### Tier 1.5 — Adjacent platforms
- [[Competitor B]]

## People to engage
- [[Founder Name]] @ [[Company]] — [why they matter]

## Open research questions
- [What you don't know yet]
- [Verticals not yet covered]
```

---

## Bases files — standard set

Four standard `.base` files should exist in the `Market Landscape/` root. Each is a YAML file with views, filters, formulas, and properties.

### Prospects DB.base

```yaml
filters: 'file.inFolder("Market Landscape/Prospects")'

formulas:
  priority_order: 'if(priority == "critical", 1, if(priority == "high", 2, if(priority == "medium", 3, 4)))'
  fit_icon: 'if(abadge_fit == "maximum", "💎 Maximum", if(abadge_fit == "high", "🔴 High", if(abadge_fit == "medium", "🟡 Medium", "🔵 Low")))'
  priority_icon: 'if(priority == "critical", "🔴 Critical", if(priority == "high", "🟠 High", if(priority == "medium", "🟡 Medium", "🟢 Low")))'
  is_agent_native: 'if(file.hasTag("agent-native"), "✅", "")'

views:
  - type: table
    name: All Prospects
    order: [file.name, formula.priority_icon, formula.fit_icon, category, funding_total, formula.is_agent_native]

  - type: table
    name: Critical Priority
    filters:
      and: ['priority == "critical"']
    order: [file.name, formula.fit_icon, category, funding_total]

  - type: table
    name: By Category
    order: [file.name, formula.priority_icon, formula.fit_icon, funding_total]
    groupBy:
      property: category
      direction: ASC

  - type: cards
    name: Cards — All
    order: [file.name, formula.priority_icon, formula.fit_icon, category, funding_total]
```

Adapt the `fit_icon` formula label to match your domain's fit property name (e.g., `abadge_fit`, `fit_score`, `relevance`).

### Competitors DB.base

```yaml
filters: 'file.inFolder("Market Landscape/Competitors")'

formulas:
  tier_label: 'if(tier == "1", "🔴 T1", if(tier == "1.5", "🟠 T1.5", if(tier == "2", "🟡 T2", "🟢 T3")))'

views:
  - type: table
    name: All Competitors
    order: [file.name, formula.tier_label, category, stage]

  - type: table
    name: By Tier
    order: [file.name, category, stage]
    groupBy:
      property: tier
      direction: ASC

  - type: cards
    name: Cards — All
    order: [file.name, formula.tier_label, category, stage]
```

### People DB.base

```yaml
filters: 'file.inFolder("Market Landscape/People")'

views:
  - type: table
    name: All People
    order: [file.name, role, company, twitter]

  - type: table
    name: Founders
    filters:
      or:
        - 'role == "Founder"'
        - 'role == "Founder & CEO"'
        - 'role == "Co-Founder & CEO"'
        - 'role == "CEO, Co-founder"'
    order: [file.name, company, twitter]

  - type: table
    name: By Company
    order: [file.name, role, twitter]
    groupBy:
      property: company
      direction: ASC
```

### Market Intelligence.base (master view)

```yaml
filters: 'file.inFolder("Market Landscape")'

formulas:
  entity_type: 'if(file.inFolder("Market Landscape/Prospects"), "🎯 Prospect", if(file.inFolder("Market Landscape/Competitors"), "⚔️ Competitor", if(file.inFolder("Market Landscape/People"), "👤 Person", if(file.inFolder("Market Landscape/Investors"), "💰 Investor", "📄 Other"))))'

views:
  - type: table
    name: Full Landscape
    order: [file.name, formula.entity_type, category, role]

  - type: table
    name: By Entity Type
    order: [file.name, category, role]
    groupBy:
      property: formula.entity_type
      direction: ASC
```

**YAML rules for .base files:**
- No duplicate map keys (e.g., never two `and:` blocks at the same level)
- Filters with a single condition: `and: ['condition']` (list, not bare string)
- `groupBy` and `filters` cannot both use the same key name at the same level

---

## Canvas design

The canvas (`landscape.canvas`) is a JSON file following the Obsidian JSON Canvas 1.0 spec.

### Layout template

```
x-axis:    -2800        -1500       -500    0      500       1800+
           Competitors  Market      Your   ICPs   Prospects  Prospects
                        Signals     Product        (T1)       (T2/T3)

y-axis:
-2000      [Segment D — newest/agent-native prospects]
-1000      [Segment C — vertical AI]
   0       [Segment A — established/funded prospects]
+1000      [Segment B — adjacent/watch-list]
```

### Node types used
- **file nodes**: `{"type": "file", "file": "path/relative/to/vault.md", ...}`
- **text nodes**: `{"type": "text", "text": "**Label**\ncontent", ...}`
- **group nodes**: `{"type": "text", "text": "Group Label", "color": "X", ...}` (positioned as background)

### Node colors
| Color | Meaning |
|-------|---------|
| 1 (red) | Critical priority / Tier 1 competitor |
| 2 (orange) | High priority / Tier 1.5 |
| 3 (yellow) | Medium priority |
| 4 (green) | Low priority / Tier 3 |
| 5 (cyan) | People / investors |
| 6 (purple) | ICPs / your product |

### Edge format
```json
{"id": "16charEdgeId00", "fromNode": "fromId", "fromSide": "right", "toNode": "toId", "toSide": "left", "label": "optional label"}
```

### Canvas generation script
`scripts/build_canvas.py` is a self-contained Python script that reads all vault notes and generates a complete canvas. Run it after major additions. It validates that all file nodes point to existing files before writing.

---

## Maintenance checklist

After adding 5+ new notes:
- [ ] Update `_Index.md` entity counts
- [ ] Add new notes to canvas (or rebuild with script)
- [ ] Check for broken wikilinks (missing linked notes)
- [ ] Verify all new notes have `research_status` set
- [ ] Ensure `last_researched` dates are populated

After adding 20+ new notes:
- [ ] Rebuild canvas with `scripts/build_canvas.py`
- [ ] Review `.base` files — do views still make sense?
- [ ] Check for duplicate notes (same company under different names)
