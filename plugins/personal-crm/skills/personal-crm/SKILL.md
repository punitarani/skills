---
name: personal-crm
description: Work with a Notion Personal CRM built on the 5-database pattern (People, Companies, Interactions, Topics, Places). Trigger whenever the user wants to add someone they just met, track an interesting person found online they haven't met yet, update contact info (email, phone, LinkedIn, Twitter, GitHub), log an interaction or meeting with notes and action items, link people via introductions or mutual connections, add companies or topics, change tier, or query the CRM to find who to follow up with, who they haven't talked to lately, who is in a specific city, at a company, or interested in a topic. Also triggers on natural phrases like "met Alice today", "add Bob to my CRM", "log my coffee with Carol", "who should I follow up with", "remind me about Dan", "interesting founder on Twitter", "find people at Stripe", or any mention of networking, introductions, contacts, or relationship management. Prefer this over generic Notion advice when the CRM is involved.
---

# Personal CRM

This skill operates a Notion Personal CRM built on a 5-database graph pattern: **People**, **Companies**, **Interactions**, **Topics**, and **Places**. It assumes the canonical schema described in `references/schema.md` (the same one produced by the reference design). The skill is the operating manual — the discovery step, the field semantics, the capture-first/enrich-later workflow, and the query recipes that actually work.

## Before doing anything

**Step 1: Load the Notion tools** (they're deferred):

```
tool_search(query="notion create page update database")
```

Work primarily with `Notion:notion-search`, `Notion:notion-fetch`, `Notion:notion-create-pages`, and `Notion:notion-update-page`.

**Step 2: Discover the user's CRM.** Every operation needs database IDs specific to the user's workspace. Do this discovery once per conversation and remember the IDs.

If the user has mentioned a CRM page URL earlier in the conversation, use that. Otherwise, search:

```
Notion:notion-search(
  query: "Personal CRM",
  query_type: "internal",
  page_size: 5
)
```

Fetch the matching page. The page content contains `<database url="..." data-source-url="collection://<ID>">Name</database>` tags for all five databases. Extract both the database URL and the data source URL for each of People, Companies, Interactions, Topics, Places.

If the search returns zero or multiple plausible matches, ask the user for the URL. Don't guess.

**Step 3: Hold the IDs in working memory** for the rest of the conversation. The skill's examples below use placeholder names like `<PEOPLE_DS_ID>` — substitute the actual discovered values in every tool call.

When setting a relation, pass the **page URL** of the related row (not the DS ID). When searching within a database, pass `data_source_url: "collection://<DS_ID>"`.

**Step 4: Know your enrichment tools.** `web_search` and `web_fetch` are always available — use them to look up people, companies, or handles when the user gave you less than they know about. Some workspaces also have specialized MCPs that do this better (Exa for research-grade web search, or dedicated LinkedIn / X / company-info servers). Run a quick `tool_search(query="linkedin profile")`, `tool_search(query="twitter x profile")`, and `tool_search(query="company lookup")` once per conversation to see what's connected. If nothing relevant is loaded but `search_mcp_registry` surfaces candidates, mention them to the user via `suggest_connectors` — don't connect them yourself. Use whatever's available. Full enrichment patterns and privacy guardrails live in `references/enrichment.md`.

## Mental model: capture first, enrich later

The system is deliberately low-friction at capture. Weekly review handles enrichment. When the user says "I met Alice today at the Stripe offsite, she works at Anthropic on evals" — you should:

1. Create the Person (Name, Status, Tier if user said one, Source, How we met, First met).
2. Create the Interaction (Title, Date, Type, People).
3. Only create/link Company or Topic or Place if the user made it clear they want that linked right now. Don't block on it — flag it as something to enrich later. Setting `Current role` as plain text is fine if the Company is known by name but not yet in the Companies DB.

A request that takes 30 seconds of user time should take 30 seconds of user time. Don't force a 10-field interrogation when they gave you 4.

## The universal fill-in-the-blank rules

Notion's API has sharp edges. These four rules cover almost every property type.

**Relations** take a **JSON array of page URLs** as a string: `"[\"https://www.notion.so/<page-id>\"]"`. If the target page doesn't exist yet, create it first, capture its URL from the response, then set the relation. For a new Person whose company isn't in the Companies DB, either (a) create the Company first if the user made it clear it's worth tracking, or (b) skip the relation and put the company name in `Current role` text field for now.

**Dates** use three expanded keys, not a single `Birthday` key:
- `"date:Birthday:start": "2026-04-21"` (ISO date)
- `"date:Birthday:end": null` (only for ranges)
- `"date:Birthday:is_datetime": 0` (use `1` only when a specific time matters — usually for Interactions.Date)

**Checkboxes** use string literals, not booleans: `"Follow-up needed": "__YES__"` or `"__NO__"`.

**Selects and multi-selects** need exact string match to existing options. If the user says "he's a founder-investor type," don't invent a new Relationship type option — pick the closest existing ones (`Founder`, `Investor`) as a multi-select array.

**Never set** these fields — they auto-calculate and rejecting them is silent:
- `Last interaction`, `Interaction count` (rollups on People)
- `Days since last contact`, `Follow-up urgency` (formulas on People)
- `Added on`, `Last edited` (system timestamps)
- Back-reference relations like `Interactions` on a Person page (auto-populated by the forward relation on Interactions.People)

Full property reference with every option, every field, every type lives in `references/schema.md` — read it when you need the exhaustive list.

## Core workflow 1: add someone the user just met

Trigger phrases: "I met X today", "add X to my CRM", "just had coffee with X", "X from [company]".

**The 30-second path.** Create the Person with only what the user actually said, set Status to `Met once` (unless the user implied closer), leave Tier empty (the 📥 Inbox view will surface it for weekly review):

```
Notion:notion-create-pages(
  parent: { data_source_id: "<PEOPLE_DS_ID>" },
  pages: [{
    properties: {
      "Name": "Alice Chen",
      "Status": "Met once",
      "How we met": "Introduced by Bob at the Stripe founder dinner on April 21, 2026",
      "Source": "Warm intro",
      "Current role": "ML engineer at Anthropic",
      "date:First met:start": "2026-04-21",
      "date:First met:is_datetime": 0,
      "LinkedIn": "https://linkedin.com/in/alicechen",
      "Email": "alice@example.com"
    }
  }]
)
```

**What to extract from natural language:**
- Name → `Name`
- Role/title → `Current role` (text, works even if Company isn't linked yet)
- How the user met them → `How we met` (write it as a full sentence with context)
- Company name mentioned → search Companies; if hit, set `Current company` relation; if miss, put it in `Current role` text and skip the relation (don't block)
- Today's date → `date:First met:start`
- Any email/phone/URL they mentioned → corresponding typed fields
- City → search Places; if hit, set `Location` relation; if miss, skip

**Inferring `Source`:** "met at a party" → `Event`, "DMed on Twitter" → `Twitter/X`, "Bob introduced me" → `Warm intro`, "reached out on LinkedIn" → `LinkedIn`. When unsure, use `Other`.

**Inferring `Tier`:** don't. Leave empty unless the user explicitly signals closeness ("my new best friend" → `Inner 5`, "just a networking contact" → `Extended 150`). Tier is meant to be a deliberate quarterly-audit decision, not a first-meeting guess.

## Core workflow 2: add an interesting person the user found online

Trigger phrases: "interesting person I found on Twitter", "add X to my radar", "want to track this founder", "potentially meet eventually", "add @handle to my CRM".

This is the workflow where enrichment earns its keep. The user often gives you just a handle, a name, or a single sentence of context — the whole point of "on radar" is you want to *know more* over time. Before creating the record, do a light enrichment pass (see Core workflow 6 and `references/enrichment.md`) to fill in real name, role, company, location, and their main URLs.

Three differences from Workflow 1:
- `Status: "Never met - on radar"`
- `How we met`: write where you found them *and note the enrichment source* — e.g. "Found via their Substack essay on mechanistic interpretability, April 2026. Profile enriched via LinkedIn."
- No `First met` date (they haven't been met)
- `Source` is usually `Twitter/X`, `LinkedIn`, `Podcast`, `Newsletter`, or `Online community`

The ✨ On radar view on People already filters to these — the user can flip through them before travel or events. Rich profiles make that flip-through actually useful.

## Core workflow 3: log an interaction

Trigger phrases: "log my coffee with X", "had a call with Y", "record that I talked to Z", "log lunch with A and B yesterday".

This is the second-most-common capture. Every interaction you log feeds the `Last interaction` rollup and the `Follow-up urgency` formula on every attendee's People page — so this is how the cadence system stays alive.

**Steps:**
1. For each named attendee: search People with `data_source_url: "collection://<PEOPLE_DS_ID>"`, query = first name or full name. If not found, either ask the user or quickly add them via workflow 1.
2. Create the Interaction, with the attendee page URLs in the `People` field.

```
Notion:notion-create-pages(
  parent: { data_source_id: "<INTERACTIONS_DS_ID>" },
  pages: [{
    properties: {
      "Title": "Coffee with Alice at Ritual — April 21",
      "date:Date:start": "2026-04-21",
      "date:Date:is_datetime": 0,
      "Type": "Coffee",
      "People": "[\"https://www.notion.so/<alice-page-id>\"]",
      "Summary": "Alice is hiring on the evals team — referred me to Mira (engineering manager). Discussed my work on mechanistic interpretability.",
      "Action items": "Send Alice my recent post; intro email to Mira by Friday",
      "Energy": "Energizing",
      "Follow-up needed": "__YES__"
    }
  }]
)
```

**What to extract from natural language:**
- Attendees → `People` (find or create)
- People who came up but weren't there ("she mentioned her cofounder Bob") → `Mentioned` (separate from `People`!) — this is how indirect graph edges form
- Companies that came up → `Companies mentioned`
- Topics — AI safety, climate, specific product — → `Topics discussed` (find or create in Topics DB)
- Summary — 2-3 sentences of what happened
- Action items → `Action items` text (keep short, user can expand later)
- If user said "draining" or "tiring" → `Energy: "Draining"`. "Great", "amazing" → `Energizing`.
- If action items exist or a next step was discussed → `Follow-up needed: "__YES__"`

**Title convention:** `{Type} with {names} — {date}` or `{Type} with {names} at {location}`. Keep it scannable — the user will skim titles in the 📅 Recent view.

## Core workflow 4: update contact info or link people

Trigger phrases: "Alice's email is …", "update Bob's LinkedIn", "Alice was introduced to me by Carol", "Bob works at Anthropic now", "remind me to follow up with Dan next week".

1. Find the Person: `notion-search` with their name and the People data source URL.
2. `notion-update-page` with `command: "update_properties"` and only the fields to change.

Setting a follow-up reminder is just updating `date:Next follow-up:start` with the target date.

To link people via self-relations:
- `Introduced by` — who introduced me to this person
- `Mutual connections` — people we both know
- `Can introduce me to` — people this person could warm-intro me to
- `Should meet` — people I want to introduce this person to

Remember: these relations are one-way by default unless the user enabled two-way sync in the Notion UI. Setting Bob as Alice's `Introduced by` does not auto-populate Alice on Bob's profile. If symmetry is wanted, set both sides or note the limitation.

## Core workflow 5: query the CRM

The user will ask things like "who should I follow up with this week?" or "who do I know at Stripe?" or "show me everyone on radar from Twitter." These map to filtered searches.

**The fast path: use the pre-built views.** The canonical build has 16 views covering common queries. Fetch the view's data source with a filter, or just direct the user to click the view. Views are listed in `references/queries.md` along with the exact filter recipes.

**The flexible path: `notion-search` with filters.** When no pre-built view covers the question, use `notion-search` scoped to the relevant data source URL. Example — "who do I know at Stripe?":

1. Find Stripe in Companies DB (search with Companies data source URL).
2. Fetch Stripe's page — the `Current people` back-relation lists everyone whose `Current company` points to Stripe.

Or — "who haven't I talked to in 6 months?" — pre-built views can't express this directly without a formula filter, so use `notion-search` on People, then fetch each result and filter by `Last interaction` in the response. For queries this complex, it's usually faster to point the user at the **💤 Revive** view.

The full query cookbook — exact filter configurations, which view to use for which question, and the `fetch` patterns for graph-traversal queries like "who has mutual connections with Alice" — lives in `references/queries.md`.

## Core workflow 6: enrich a profile with external data

Trigger phrases: "look him up on LinkedIn", "find her Twitter", "who is @handle", "fill in what you can find about X", "brief me on Y before the meeting", or whenever the user gave you less info than you need and the gap is fillable from public sources.

**When to enrich automatically (don't ask):**
- Workflow 2 (on-radar) — enrichment is the whole point. User gave you a handle or one-liner; fill in the professional basics.
- Pre-meeting briefings — fetch recent public activity (last month of posts, recent news mentions, career moves) to surface fresh conversation fuel.
- Explicit lookups — user says "find Bob's LinkedIn," just do it.

**When to ask first:**
- Inner 5 / Close 15 tier. These are personal contacts the user already knows intimately; web-searching them feels off. Ask: "Want me to skip the lookup since you know them well, or is there something specific you want me to find?"
- When you don't know which person the user means (common name, no context).

**When NOT to enrich:**
- When the user explicitly wants speed ("just capture her name, I'll fill the rest later").
- For anyone whose Status is `Do not contact`.
- When the user says "don't google them" or equivalent.

### The enrichment loop

1. **Pick the right tool.** Check what's available. MCPs specifically for LinkedIn or X will return cleaner structured data than web search. Exa is excellent for people-research when connected. Fall back to `web_search` + `web_fetch` otherwise.

2. **Query wisely.** If you have a handle, search for it. If you have a name + weak context, combine them: "Maya Rodriguez Linear design" beats "Maya Rodriguez" alone. Two or three queries max per person — this is light enrichment, not investigation.

3. **Extract only publicly-professional info:** real name, current role, current company, city, headline/bio, public URLs (LinkedIn, X, GitHub, personal site). Skip anything that feels private — personal phone numbers or home addresses you stumbled into, drama, old posts out of context.

4. **Write to the CRM with attribution.** In `How we met` or append to the page body: "Profile enriched via LinkedIn on [date]." This matters — future-you needs to know which facts came from the user's direct knowledge vs. from a web fetch. Also useful if facts later turn out wrong.

5. **Report what changed.** In your reply, clearly distinguish what the user told you from what enrichment added: *"Added Neel Nanda (as you described). From LinkedIn: he's a researcher at DeepMind in London, works on mechanistic interpretability."*

### Detailed enrichment recipes

Patterns for handle → profile, name → LinkedIn, company enrichment, and pre-meeting recent-activity lookups live in `references/enrichment.md`. Read that when the enrichment gets non-trivial, when a lookup returns ambiguous results, or when the user asks for the deep-briefing variant.

## Finding existing pages

Before creating anything, search. The CRM rewards linking over duplicating.

```
Notion:notion-search(
  query: "Alice",
  query_type: "internal",
  data_source_url: "collection://<PEOPLE_DS_ID>",
  page_size: 5
)
```

Scope by `data_source_url` so you're searching one database at a time. Full-workspace searches return noise. If there are multiple matches (common with first names), show them to the user and ask.

## Patterns for composing multiple writes

Real user requests often involve several steps. Three examples of the "orchestration" pattern:

**"I had coffee with Alice at Ritual yesterday and she introduced me to her cofounder Bob who's working on climate tech."**

1. Find or create Alice in People.
2. Find or create Bob in People (Status: `Met once`, `Introduced by: Alice-page-url`).
3. Optionally create or find `Climate tech` in Topics; link to Bob's `Topics`.
4. Create Interaction: `People: [Alice]`, `Mentioned: [Bob]`, `Type: Coffee`, location Ritual (find or create in Places), Summary mentions the intro.

**"Log my standup with the eng team — me, Priya, and Marco. We talked about the latency regression and Marco's taking the fix."**

1. Find Priya and Marco (they almost certainly exist in Colleague tier).
2. Create Interaction: `Type: Video call`, `People: [Priya, Marco]`, `Summary`: latency regression discussion, `Action items`: "Marco: fix latency regression", `Follow-up needed: __YES__`.

**"Add three people I want to track: @swyx on Twitter (AI engineer), Sarah Constantin (rationalist blogger), and Dwarkesh Patel (podcaster)."**

Three sequential create-Person calls, all with `Status: "Never met - on radar"`, appropriate `Source` values, and `How we met` capturing where the user found them. Don't try to batch-create in one call if you need each URL back for future reference — do them one at a time.

## Tier cadence reference (in the canonical formula)

The `Follow-up urgency` formula derives overdue status from tier + last-interaction date. Thresholds:

| Tier | Contact within | Who belongs |
|---|---|---|
| Inner 5 | 14 days | Closest people |
| Close 15 | 30 days | Good friends & collaborators |
| Network 50 | 90 days | Active professional network |
| Extended 150 | 180 days | Occasional broader network |
| Periphery | no cadence | Deliberately low-maintenance |

Knowing this lets you answer "is this urgent?" without a round-trip. If the user hasn't talked to a Close-15 person in 5 weeks, that's Overdue. (If the user has customized the formula, these thresholds may differ — check the People DB's `Follow-up urgency` formula property if their answers disagree with yours.)

## When to read the reference files

- **`references/schema.md`** — when you need the complete, authoritative field list for any database. All select options. All relations. All back-references. Read this when the user asks for a field you're not 100% sure of.
- **`references/queries.md`** — when the user asks a query question and you're not sure which view matches or how to write the filter. Covers all 16 pre-built views and recipes for common freeform queries.
- **`references/enrichment.md`** — when you're enriching a profile with external data. Has the handle-to-profile pattern, name-disambiguation recipes, company enrichment, pre-meeting briefing recipes, and the privacy guardrails.
- **`references/edge-cases.md`** — when something breaks, when the user asks to do something unusual, or when you need the exhaustive list of gotchas (the formula/rollup self-reference bug, the self-relation DDL quirk, how to handle name collisions, etc.).

## What this skill is not for

- Creating new databases, tables, or schema changes. This skill assumes the CRM is already built.
- Generic Notion advice unrelated to this CRM. Use general Notion knowledge for that.
- Bulk imports from CSV or other systems — use the Notion UI's built-in import, or ask the user first before scripting it.
- CRMs with significantly different schema (e.g., only People + Companies, or different field names). The schema reference assumes the canonical build; if the user's setup diverges substantially, adapt — principles still apply but specific field names won't match.

## Golden rules

1. **Discover IDs once per conversation.** Don't re-search on every action.
2. **Respect capture friction.** A 4-field request produces a 4-field row. Don't interrogate.
3. **Link, don't duplicate.** Search before you create.
4. **Never touch auto-calculated fields.** Rollups, formulas, timestamps are read-only.
5. **The `Mentioned` field on Interactions is the most underused and most valuable.** Use it aggressively when people come up in conversation without being present.
6. **If unsure of a select-option value, look it up in `schema.md` rather than guessing.** Inventing new option values silently fails.
7. **Enrich with attribution, not stealth.** When external data goes into the CRM, note the source and date in `How we met` or the page body. Keep enrichment light — 2-3 queries per person, professional-public only, skip the Inner 5 unless asked.
