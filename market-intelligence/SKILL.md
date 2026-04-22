---
name: market-intelligence
description: >
  Build, enrich, verify, and activate structured competitive intelligence in Obsidian vaults.
  ALWAYS use for: researching companies or markets, building prospect/competitor/people notes,
  deep-diving a vertical, finding companies that need a product, tracking founders or investors,
  verifying social handles are real and active, building outreach lists or HTML contact trackers,
  mapping relationships to find warm intro paths. Triggers on "market landscape", "competitive
  analysis", "research companies", "find competitors", "deep dive into X space", "prospect
  research", "verify these handles", "check if these profiles are real", "build an outreach list",
  "who should I reach out to", "map my contacts", "find warm intros", "relationship graph",
  "add to my vault", "enrich my knowledge base". Any domain: SaaS, AI, fintech, biotech, etc.
---

# Market Intelligence Skill

Build, enrich, verify, and activate structured competitive intelligence — stored in Obsidian vaults,
exported as interactive HTML, or mapped as relationship graphs. This skill is opinionated about
structure (consistent frontmatter, semantic tagging, scored entities, verified contacts) but adapts
to any domain, product, or research context.

## Before you start — load the right references

| Reference | Load when |
|-----------|-----------|
| `references/note-schemas.md` | Before creating ANY note |
| `references/research-playbook.md` | When researching a new entity type |
| `references/vault-structure.md` | Creating structure, canvas, or bases |
| `references/social-verification.md` | Running Verify mode or checking handles |
| `references/outreach-list.md` | Building outreach lists or HTML artifacts |

Only load what's needed — don't read all five for a simple enrichment task.

---

## Modes

Determine which mode the user needs, then jump straight in. Don't ask unnecessary questions — infer from context. Multiple modes can be combined (e.g., Enrich → Verify → Outreach in one session).

| Mode | When to use | Core action |
|------|-------------|-------------|
| **Bootstrap** | Starting from scratch, no vault exists | Create structure → research initial entities in parallel |
| **Enrich** | Vault exists, adding or deepening notes | Research → write notes → update index |
| **Deep Dive** | "Go deep on X vertical / space" | Spawn parallel research agents → synthesize |
| **Verify** | "Check these handles", "are these people real", suspicious/stale contacts | Navigate to profiles → flag wrong/inactive → find replacements |
| **Outreach** | "Build me an outreach list", "who should I contact", export contacts | Pull vault people → rank → generate HTML artifact |
| **Graph** | "Map my relationships", "find warm intros", "who connects to who" | Scan wikilinks → build adjacency map → identify paths |
| **Search** | "Find companies that need X", "who are the players in Y" | Research → filter → ranked shortlist |
| **Maintain** | Rebuild canvas, update bases, refresh index | Structural updates without new research |

---

## Mode: Bootstrap

Starting a new intelligence vault from zero.

### What to gather (from context or by asking once)
- **Product or context**: What is the user building or analyzing?
- **Domain**: What market? (e.g., "AI developer tools", "fintech compliance")
- **Seed companies**: Any companies they already know?
- **Vault path**: Where should the vault live on disk?
- **Scoring lens**: What makes a company a good fit or threat?

Don't ask for things you can infer. If someone says "I'm building a credential API for AI agents", you already know the domain, scoring lens, and ICP shape.

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
Domain overview, market signals, entity counts, key findings. Keep scannable — this is the vault entry point.

**Step 3 — Define ICPs**
Create 2–4 ICP notes in `ICPs/`. ICPs define who the ideal buyers/users are and guide prospect scoring. See schema in `references/note-schemas.md`.

**Step 4 — Parallel company research**
For each seed company (and 10–20 more found via web search), spawn parallel research subagents. See **Parallelization** section below. Pass the note schema to every agent.

**Step 5 — Build canvas and bases**
After notes exist, generate `landscape.canvas` using `scripts/build_canvas.py` and create the four standard `.base` database views (see `references/vault-structure.md`).

---

## Mode: Enrich

Adding to an existing vault.

**Step 1 — Audit (quick)**
Read 3–5 existing notes to understand: which properties are in use, what's already covered, schema conventions established.

**Step 2 — Research and write**
For each new entity:
1. Read `references/research-playbook.md` for that entity type
2. Web search for current information
3. Write the note — completeness over speed
4. Add wikilinks to existing notes

**Step 3 — Update structural files**
After adding 5+ entities: update `_Index.md`. Offer to rebuild `landscape.canvas` and `.base` files.

---

## Mode: Deep Dive

Intensive focused research on a specific vertical.

**Step 1 — Confirm scope**
One question if needed: which exact vertical or sub-domain?

**Step 2 — Spawn parallel research agents**
For a full deep dive, spawn 4–6 subagents simultaneously:
- Agent 1: Category leaders and direct players
- Agent 2: Adjacent companies that could expand in
- Agent 3: Recent YC/seed-stage startups (last 18 months)
- Agent 4: Key investors and portfolio companies
- Agent 5: Founders/thought leaders defining the space
- Agent 6: International or non-obvious entrants

Each agent writes notes directly to the vault and returns a summary.

**Step 3 — Synthesize**
Write `Intel/[Vertical Name] Deep Dive.md`:
- Key themes and signals
- Competitive dynamics
- Top recommended prospects with scores
- Open questions

---

## Mode: Verify

**Purpose**: Ensure every contact in a list is real, active, and correctly attributed before any outreach. This is critical — hallucinated or stale handles waste outreach effort and embarrass the sender.

Read `references/social-verification.md` before starting this mode.

### When to use
- Before exporting any outreach list
- After generating research with subagents (always verify)
- When auditing an existing list for stale/wrong contacts
- When any contact feels uncertain ("I found this handle but...")

### What "verified" means
- ✅ Profile exists at the expected URL
- ✅ Name on the profile matches the intended contact
- ✅ Bio/employer matches expected company
- ✅ Account has recent activity (within 6 months) and credible follower count (100+)

### Verification workflow

**Step 1 — Triage the list**
Scan the contact list and flag anyone that looks uncertain:
- Handles found via web search (not from a primary source like team page or GitHub bio)
- People with common names (handle could belong to someone else)
- Handles with unusual patterns (trailing numbers, underscores)
- Anyone added without a direct URL to their profile

**Step 2 — Verify via browser (Chrome MCP preferred)**
For each contact, navigate to the profile and read page text:
```
Navigate to: https://x.com/{handle}  (or linkedin.com/in/{handle})
Check: displayed name, bio keywords, employer mention, follower count
```
Use `mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text`.
If Chrome MCP is unavailable, use Playwright (`playwright navigate`, `playwright get_visible_text`).

**Step 3 — Classify each contact**
| Status | Meaning | Action |
|--------|---------|--------|
| ✅ Verified | Name + bio match, account active | Keep as-is |
| ⚠️ Low confidence | Name matches but bio unclear, few followers | Web search to confirm |
| ❌ Wrong person | Name on profile ≠ expected contact | Find correct handle |
| ❌ Inactive | 0–50 followers, no posts, placeholder bio | Replace or mark stub |
| ❌ Doesn't exist | 404 / "account doesn't exist" | Find real handle or remove |

**Step 4 — Find replacements**
For any contact that failed:
1. Web search: `"[Full Name]" "[Company]" Twitter OR "X.com"`
2. Check the company team page, GitHub profile, LinkedIn
3. Cross-reference from mutual contacts' profiles
4. If no handle found: update note with `handle_verified: false`, note the gap

**Step 5 — Evaluate replacement quality**
Before adding a replacement or replacing a wrong person entirely:
- Does the replacement serve the same strategic purpose?
- Is their account active (last post within 3 months)?
- Is their follower count credible (100+ for founders, 500+ for thought leaders)?
- Do they have relevance to your product/domain?

**Step 6 — Update notes and report**
- Update `twitter`, `linkedin`, or relevant handle field in the note
- Set `handle_verified: true` and `handle_verified_date: YYYY-MM-DD`
- Add a note if the contact was replaced: `> Previously listed as [wrong name]. Corrected on [date].`

Produce a verification summary:
```
Verified: X/Y contacts
Fixed handles: [list]
Replaced contacts: [list with reason]
Unable to verify: [list with what was tried]
```

---

## Mode: Outreach

**Purpose**: Turn vault intelligence into an actionable, prioritized contact list — optionally with an interactive HTML artifact for search, filter, and tracking.

Read `references/outreach-list.md` before building a list.

### When to use
- "Build me an outreach list from my vault"
- "Who should I reach out to this week?"
- "Create a searchable contact sheet"
- "Generate an HTML tracker for my prospects"

### Workflow

**Step 1 — Define scope**
Clarify (from context or one question):
- Which entity types to include: Prospects (company contacts), People, Investors, all?
- Filter: by priority, by tag, by company type, or all?
- Platform: Twitter/X, LinkedIn, email, or multi-platform?
- Format: simple ranked list, or interactive HTML artifact?

**Step 2 — Pull and rank contacts**
Scan `People/` and `Prospects/` notes. For each contact:
- Extract: name, role, company, handles, priority, tags, outreach angle
- Rank by: priority score, fit score, recency of signal, relationship warmth
- Group into logical sections (e.g., "Infrastructure Founders", "Key Investors", "Developer Advocates")

**Step 3 — Verify before exporting**
Run Verify mode on the contact list before finalizing. A single wrong handle destroys credibility.

**Step 4 — Generate output**

For a **simple list**: ranked markdown table with name, company, handle, one-line angle.

For an **interactive HTML artifact**: use `scripts/gen_outreach_html.py` or build programmatically.
See `references/outreach-list.md` for the full HTML structure and schema.

The HTML artifact should include:
- Dark-themed, professional appearance
- Search bar filtering across name, company, role, tags
- Section tabs or filter buttons (by tier, category, platform)
- Per-contact cards: name, role, company, handle (with click-to-profile link), priority badge, outreach angle
- Copy-to-clipboard for handles and DM openers

**Step 5 — Craft outreach angles**
For each person, the outreach angle is the most important field — one specific reason this person will respond. Draw from:
- Their recent public signal (launch, blog post, tweet, funding)
- A specific pain point their company has that your product solves
- Something they've said publicly that you can respond to directly

Generic angles ("I'd love to connect!") will be ignored. Specific angles get replies.

---

## Mode: Graph

**Purpose**: Map the relationship network across vault entities, identify clusters, and find warm introduction paths.

### Workflow

**Step 1 — Scan wikilinks**
Parse all notes for `[[wikilinks]]`. Build an adjacency list:
```
Person A → works at → Company X
Company X → funded by → Investor Y
Investor Y → known partner → Person B
```

**Step 2 — Build the adjacency map**
Dictionary: `{entity: [(connected_entity, relationship_type)]}`.

**Step 3 — Find intro paths**
For a target contact, run BFS to find chains:
```
You → [shared connection] → [target]
```
Surface paths of length 2 (one hop) and length 3 (two hops). Longer paths are rarely actionable.

**Step 4 — Identify clusters**
Group entities: companies with shared investors, founders with shared backgrounds, YC batch cohorts. These are natural outreach communities — know one, get warm intros to the rest.

**Step 5 — Export**
- As an Obsidian canvas (via `scripts/build_canvas.py` with relationship edges)
- As `Intel/Relationship Map.md` with the full adjacency list
- As a text summary: "Warm paths to [Target]" with the connection chain

---

## Mode: Search

Find companies matching criteria without necessarily adding them to the vault.

1. Clarify: company type, problem they must have, stage/size/geography
2. Web search: YC batches, funding announcements, vertical lists
3. Score each against user's criteria
4. Return ranked shortlist, ask which to add to vault

---

## Mode: Maintain

Structural updates only.

- **Canvas**: Run `scripts/build_canvas.py` → write to `landscape.canvas`
- **Bases**: Use `obsidian:obsidian-bases` skill for `.base` files
- **Index**: Count entities, update `_Index.md`

---

## Parallelization

Use subagents when researching 5+ companies or multiple verticals. Spawn all together in one message — never sequentially.

### Company research agent prompt template
```
You are researching [Company Name] for a market intelligence vault about [domain/product context].

Task: Write a complete Obsidian note for this company.
Output file: [vault-path]/Market Landscape/[Prospects or Competitors]/[Company Name].md

Note schema (copy frontmatter exactly, fill in values):
[paste relevant schema from references/note-schemas.md]

Scoring criteria:
- fit_score: maximum = can't operate without it | high = strong near-term need | medium = eventual need | low = tangential
- priority: critical = reach out this week | high = this month | medium = this quarter | low = watch

Research requirements:
1. Product description (1–2 sentences)
2. Customer profile and scale
3. Funding (total, last round, investors, date)
4. Founders (names, backgrounds, Twitter/X handles, LinkedIn)
5. Why [our product] matters to them (specific mechanism)
6. Recent strategic signal (launch, pivot, partnership, hiring — dated)

Set research_status: needs-update if you cannot find enough to fill the note.
```

### Verification agent prompt template
```
You are verifying a batch of [platform] handles for a market intelligence vault.

For each contact below, navigate to their profile and confirm:
1. Profile exists at the URL (not 404)
2. Displayed name matches the expected contact
3. Bio/employer mentions expected company
4. Account has posts and credible follower count (>100)

If a handle fails, search: "[Full Name]" "[Company]" site:twitter.com
Also check the company team page for correct handles.

Contacts to verify:
[list: name | company | handle | profile URL]

Return a verification report: verified / fixed / replaced / unable-to-verify for each.
Write handle corrections directly to Person notes at [vault-path].
```

---

## Scoring Framework

Always assign real scores — vague notes are useless.

### Fit Score

| Score | Meaning |
|-------|---------|
| `maximum` | Can't operate without your product. Core to their business model, active pain, no workaround. |
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

### Outreach Tier

| Tier | Meaning |
|------|---------|
| `A` | Reach out this week — high fit + verified active + strong angle |
| `B` | Reach out this month — good fit, verified, angle available |
| `C` | Warm up first — follow/engage before cold outreach |
| `D` | Watch — worth tracking, not yet ready to contact |

---

## Research Quality Standards

Every company note must answer:
1. What do they build? (1–2 sentences, no marketing fluff)
2. Who are their customers? (profile + scale)
3. How are they funded? (total, last round, date, lead investor)
4. Who leads it? (CEO + founders, backgrounds, social handles)
5. Why does our product matter to them? (specific mechanism, not generic)
6. What's the freshest signal? (launch, pivot, partnership — dated, within 12 months)

Never publish a sparse note. If info is missing, set `research_status: needs-update`.

---

## Wikilinks — Always Link

- Prospect notes → link investor names to `Investors/` notes
- Prospect notes → link competitor names to `Competitors/` notes
- Person notes → link to their company note
- Use `[[Name]]` syntax — exact filename match

Check what exists before creating new notes to avoid duplicates.

---

## Tagging Conventions

Use semantic tags for cross-vault filtering. Examples:
- Domain: `ai-agent`, `browser-automation`, `mcp-ecosystem`, `dev-infra`, `fintech`
- Signal: `yc-w25`, `recently-funded`, `recently-launched`, `hiring-fast`
- Contact: `open-to-dm`, `founder-led`, `active-on-x`, `thought-leader`
- Relationship: `warm-intro-available`, `investor-overlap`
- Verification: `handle-verified`, `handle-unverified`, `contact-replaced`

---

## Canvas Design Principles

- **Layout**: Competitors left (x < -1000), your product center (x ≈ 0), Prospects right (x > 500)
- **Grouping**: Cluster prospects by segment using group nodes
- **Color coding**: critical = color 1 (red), high = 2 (orange), medium = 3 (yellow), low = 4 (green)
- **Edges**: Connect people → companies, companies → investors, investors → portfolio
- **Scale**: For 20+ notes, use `scripts/build_canvas.py` — hand-coding at scale breaks

---

## Browser Automation Tools

For Verify mode and real-time research, use tools in this order:

1. **Chrome MCP** (`mcp__Claude_in_Chrome__*`) — fastest for quick profile checks
   - `navigate` → go to profile URL
   - `get_page_text` — extract visible text (name/bio/followers)

2. **Playwright MCP** (if installed) — more powerful for complex workflows
   - Handles JavaScript-rendered pages better
   - Can extract structured data from profile cards

3. **WebSearch / WebFetch** — fallback for finding handles when profiles are wrong
   - Search: `"[Full Name]" "[Company]" site:twitter.com OR site:x.com`

Never trust a handle found only via web search without navigating to the actual profile.

---

## Reference Files

| File | Load when |
|------|-----------|
| `references/note-schemas.md` | Before creating ANY note |
| `references/research-playbook.md` | When researching a new entity type |
| `references/vault-structure.md` | Creating structure, canvas, or bases |
| `references/social-verification.md` | Running Verify mode, checking handles |
| `references/outreach-list.md` | Building outreach lists or HTML artifacts |
| `scripts/build_canvas.py` | Rebuilding the visual canvas map |
| `scripts/gen_outreach_html.py` | Generating interactive HTML outreach tools |
