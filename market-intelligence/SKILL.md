---
name: market-intelligence
description: >
  Build, enrich, and search a structured competitive intelligence knowledge base in Obsidian.
  ALWAYS use this skill when the user wants to research companies in a market, map a competitive
  landscape, add prospects or competitors to a vault, do a deep dive into a vertical or domain,
  enrich existing company notes, find companies that would need a given product, track key people
  (founders, investors), or build any kind of organized market research. Triggers on "market
  landscape", "competitive analysis", "research companies", "find competitors", "add to my vault",
  "deep dive into X space", "who are the key players", "prospect research", "build intelligence on",
  "enrich my knowledge base", "find companies that need X", "research the Y vertical", "add a note
  for company Z". Works for any domain: SaaS, AI, fintech, biotech, consumer, dev tools, etc.
---


# Market Intelligence Skill

Build, enrich, and explore structured competitive intelligence vaults in Obsidian — from scratch or on top of an existing vault. This skill is opinionated about structure (consistent frontmatter, semantic tagging, scored entities) but adapts to any domain or product.

## Before you start — load these references

Always read the relevant references before creating notes or running research:
- `references/note-schemas.md` — Frontmatter schemas for all entity types (Prospect, Competitor, Person, Investor, ICP). **Load before creating any note.**
- `references/research-playbook.md` — What to look for when researching each entity type, source priority, research depth requirements.
- `references/vault-structure.md` — Folder layout, naming conventions, canvas patterns, .base file conventions.

Only load what's needed for the current task — don't load all three if you're just enriching one note.

---

## Modes

Determine which mode the user needs, then jump straight in. Don't ask unnecessary questions — infer from context.

| Mode | When to use | Core action |
|------|-------------|-------------|
| **Bootstrap** | Starting from scratch, no vault exists | Create structure → research initial companies in parallel |
| **Enrich** | Vault exists, adding entities or deepening existing notes | Research new companies/people → write notes → update index |
| **Deep Dive** | "Go deep on X vertical" or "research the Y space" | Spawn parallel vertical research agents → synthesize findings |
| **Maintain** | Rebuild canvas, update bases, refresh index | Structural updates without new research |
| **Search** | "Find companies that need X" or "who are the players in Y" | Research → filter → present scored shortlist |

---

## Mode: Bootstrap

Starting a new vault from zero.

### What to gather (from context or by asking once)
- **Product or context**: What is the user building or analyzing?
- **Domain**: What market? (e.g., "AI developer tools", "fintech compliance")
- **Seed companies**: Any companies they already know?
- **Vault path**: Where should the vault live on disk?
- **Scoring lens**: What makes a company a good fit/threat?

Don't ask for things you can infer — if they say "I'm building Abadge, a credential vault for AI agents", you already know the domain, scoring lens, and category of prospects.

### Workflow

**Step 1 — Create vault structure**
```
{vault-root}/
├── Market Landscape/
│   ├── Prospects/          # Target companies / potential customers
│   ├── Competitors/        # Competing or adjacent companies
│   ├── People/             # Founders, investors, key influencers
│   ├── Investors/          # VC firms and angels active in the space
│   ├── ICPs/               # Ideal customer profiles
│   └── Intel/              # Thematic research, maps, signals
├── _Index.md               # Master index (auto-maintained)
└── landscape.canvas        # Visual map (build after notes exist)
```

**Step 2 — Write _Index.md**
Include: domain overview, market signals, entity counts per category, key findings. Keep it scannable — this is the entry point to the vault.

**Step 3 — Define ICPs**
Create 2–4 ICP notes in `ICPs/`. ICPs define WHO the ideal buyers/users are and guide prospect scoring. See schema in `references/note-schemas.md`.

**Step 4 — Parallel company research**
For each seed company (and 10–20 more found via research), spawn parallel research subagents. See **Parallelization** section below. Pass the note schema to every agent.

**Step 5 — Build canvas and bases**
After notes exist, generate `landscape.canvas` using `scripts/build_canvas.py` and create the four standard `.base` database views (see `references/vault-structure.md`).

---

## Mode: Enrich

Adding to an existing vault.

### Workflow

**Step 1 — Audit (quick)**
Scan existing notes to understand: what properties are in use (read 3–5 sample notes), what's already covered (avoid duplicates), schema conventions established.

**Step 2 — Research and write**
For each new entity:
1. Read `references/research-playbook.md` for the entity type
2. Web search for current information
3. Write the note using the schema — completeness over speed
4. Add wikilinks to existing notes (people → company, company → investors)

**Step 3 — Update structural files**
After adding 5+ entities, update `_Index.md`. Offer to rebuild `landscape.canvas` and `.base` files.

---

## Mode: Deep Dive

Intensive focused research on a specific vertical or domain.

### Workflow

**Step 1 — Confirm scope**
One question if needed: which exact vertical or sub-domain?

**Step 2 — Spawn parallel vertical research agents**
For a full deep dive, spawn 4–6 subagents simultaneously, each covering a different angle:
- Agent 1: Category leaders and direct players
- Agent 2: Adjacent companies that could expand in
- Agent 3: Recent YC/seed-stage startups (last 18 months)
- Agent 4: Key investors and portfolio companies
- Agent 5: Founders/thought leaders defining the space
- Agent 6: International or non-obvious entrants

Each agent writes notes directly to the vault and returns a summary.

**Step 3 — Synthesize**
Write a synthesis note in `Intel/[Vertical Name] Deep Dive.md`:
- Key themes and signals
- Competitive dynamics
- Top recommended prospects with scores
- Open questions

---

## Mode: Maintain

Structural updates only — no new research.

- **Canvas**: Run `scripts/build_canvas.py` → write output to `landscape.canvas`
- **Bases**: Use `obsidian:obsidian-bases` skill to create/update the four standard `.base` files
- **Index**: Count entities, update `_Index.md`

---

## Mode: Search

Find companies matching criteria without necessarily adding them to the vault.

1. Clarify: what type of company, what problem they must have, what stage/size/geography
2. Web search for candidates — YC batches, funding announcements, vertical lists
3. Score each against the user's product/criteria
4. Return ranked shortlist, ask which to add to vault

---

## Parallelization

Use subagents when researching 5+ companies or covering multiple verticals. Spawn them all together in one message — never sequentially.

### Company research agent prompt template
```
You are researching [Company Name] for a market intelligence vault about [domain/product context].

Task: Write a complete Obsidian note for this company.
Output file: [vault-path]/Market Landscape/[Prospects or Competitors]/[Company Name].md

Note schema (copy frontmatter exactly, fill in values):
[paste relevant schema from references/note-schemas.md]

Scoring criteria:
- fit score: maximum = can't operate without it | high = strong near-term need | medium = eventual need | low = tangential
- priority: critical = reach out this week | high = this month | medium = this quarter | low = watch

Research requirements:
1. Product description (1–2 sentences)
2. Customer profile and scale
3. Funding (total, last round, investors, date)
4. Founders (names, backgrounds, social handles)
5. Why [our product] matters to them (specific mechanism)
6. Recent strategic signal (launch, pivot, partnership, hiring — dated)

Set research_status: needs-update if you cannot find enough to fill the note.
```

### Vertical research agent prompt template
```
You are researching the [vertical] space for a market intelligence vault.

Task: Find 5–8 companies in [vertical] that [specific criteria].
For each, write an Obsidian note at: [vault-path]/Market Landscape/Prospects/[Company Name].md

Use this frontmatter schema: [paste Prospect schema from references/note-schemas.md]

Focus on signals like: [domain-specific signals]

Return a brief summary: companies found, key insight about vertical, most interesting finding.
```

---

## Scoring Framework

Always assign real scores — vague notes with no scoring are useless.

### Fit Score (adapt label to domain)

| Score | Meaning |
|-------|---------|
| `maximum` | Can't operate without your product. Core to business model, active pain, no workaround. |
| `high` | Strong need, plausible near-term buyer. Clear use case, credible budget. |
| `medium` | Would benefit but workarounds exist. Not urgent. |
| `low` | Tangential use case. Edge scenarios only. |

### Priority Score

| Score | Timeline |
|-------|----------|
| `critical` | This week — high fit + recent trigger signal |
| `high` | This month — high fit, no immediate trigger |
| `medium` | This quarter — medium fit or early stage |
| `low` | Watch and wait |

### Competitor Tier

| Tier | Meaning |
|------|---------|
| `1` | Direct threat — same customer, same problem |
| `1.5` | Adjacent platform that could expand into your space |
| `2` | Same buyer, different problem — could bundle or compete |
| `3` | Legacy incumbent — established but slow-moving |

---

## Research Quality Standards

Every company note must answer:
1. What do they build? (1–2 sentences, no marketing fluff)
2. Who are their customers? (profile + scale)
3. How are they funded? (total, last round, date, lead investor)
4. Who leads it? (CEO + founders, backgrounds, social handles)
5. Why does our product matter to them? (specific mechanism)
6. What's the freshest signal? (launch, pivot, partnership — dated)

Never publish a sparse note. If info is missing, set `research_status: needs-update` and note the gaps.

---

## Wikilinks — Always Link

- Prospect notes → link investor names to `People/` or `Investors/` notes
- Prospect notes → link competitor names to `Competitors/` notes
- Person notes → link to their company note
- Use `[[Company Name]]` syntax — exact filename match

Check what already exists before creating new person/investor notes to avoid duplicates.

---

## Tagging Conventions

Use semantic tags that enable cross-vault filtering. Examples (adapt to domain):
- `credential-custody` — handles credentials on behalf of users
- `agent-native` — built for AI agents, not just humans
- `mcp-ecosystem` — builds with or on Model Context Protocol
- `browser-agent` — automates browser actions as an agent
- `per-client-isolation` — separate credentials per end user
- `yc-w25` — YC Winter 2025 cohort

Tags drive filter views in Bases files. They're the primary way to slice the vault without writing queries.

---

## Canvas Design Principles

- **Layout**: Competitors left (x < -1000), your product center (x ≈ 0), Prospects right (x > 500)
- **Grouping**: Cluster prospects by segment using group nodes
- **Color coding**: critical = node color 1 (red), high = 2 (orange), medium = 3 (yellow), low = 4 (green)
- **Edges**: Connect people → companies, companies → investors
- **Scale**: For 20+ notes, use `scripts/build_canvas.py` — hand-coding at scale breaks

---

## Reference Files

| File | Load when |
|------|-----------|
| `references/note-schemas.md` | Before creating ANY note |
| `references/research-playbook.md` | When researching a new entity type |
| `references/vault-structure.md` | Creating structure, building canvas, or setting up bases |
| `scripts/build_canvas.py` | Rebuilding the visual canvas map |
