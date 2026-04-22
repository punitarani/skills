# Personal CRM — Enrichment patterns

When and how to use `web_search`, `web_fetch`, Exa, or dedicated LinkedIn/X MCPs to fill in what the user didn't tell you. Covers the common recipes, the judgment calls, and the privacy guardrails.

## Tool priority

Use whichever tool gives the best signal for the smallest cost. Rough priority:

1. **Dedicated MCPs** (LinkedIn, X/Twitter, company-info servers) if connected. These return structured data — no parsing from search result snippets. Check via `tool_search(query="linkedin profile")` / `tool_search(query="twitter x user")` / `tool_search(query="company lookup")` at the start of a conversation.
2. **Exa** if connected — built for AI research queries, better recall than generic search for people lookup.
3. **`web_search`** — always available. Good for general discovery ("what's their role?") and disambiguation.
4. **`web_fetch`** — when you have a specific URL (a LinkedIn profile, a personal site, an About page) and want the full contents.

If no MCP is loaded but `search_mcp_registry` surfaces a relevant one, mention it via `suggest_connectors` — don't connect it yourself. Example: "If you connect the LinkedIn MCP I could pull profile data more cleanly. Want me to suggest it?"

## The core decision: enrich or skip?

Before any search, ask yourself:

**Enrich when any of these are true:**
- The person is being added to the `Never met - on radar` bucket (Workflow 2). Enrichment is the whole point.
- The user gave you just a handle, a first name + role, or a one-line description and the gap is obviously fillable.
- The user explicitly asked ("look them up," "find their LinkedIn," "who is @karpathy").
- You're prepping a briefing for a tier Network 50 or below (the user doesn't know them well enough to self-brief).

**Skip enrichment when:**
- The person is Inner 5 / Close 15 and the user is just asking you to record something — they know them better than any search will reveal. Asking "want me to web-enrich your best friend" is weird. If enrichment is needed for a close contact (rare), ask first.
- The user said "quick," "just capture," or otherwise signaled speed.
- The person's Status is `Do not contact`.
- Search returns nothing useful after two tries. Don't escalate to aggressive search — the answer is "limited public footprint" and that's fine.

When in doubt about a close contact, ask. Better to check than to silently web-search the user's sister.

## Recipe 1: Handle → full profile

Input: `@karpathy`, `@pmarca`, `linkedin.com/in/something`.

Steps:
1. If it's a LinkedIn URL, `web_fetch` the URL directly (LinkedIn public profiles render with substantial info).
2. If it's an X/Twitter handle, search `web_search("@karpathy twitter bio")` or use a dedicated X MCP. Extract: real name, bio, location, headline, linked websites.
3. Optionally: one more search with the real name + a distinguishing detail for secondary info (GitHub? Personal site?).

Write to People:
- `Name`: real name from enrichment
- `X / Twitter` or `LinkedIn`: the URL
- `Current role`: parsed from bio/headline
- `Current company`: if stated in bio and worth linking (otherwise just in `Current role` text)
- `Website`: if they have one
- `How we met`: "Found via X handle @karpathy — profile enriched via [source] on [date]"
- `Source`: `Twitter/X` (or wherever you found them)

Topics: if bio mentions specific fields (AI, climate, neuroscience), create/link relevant Topics.

## Recipe 2: Name + weak context → disambiguate and enrich

Input: "this PM at Stripe called Maya," "Dan who works in climate tech."

Steps:
1. Search: combine all clues. `web_search("Maya Stripe PM")` returns much better results than just "Maya."
2. If the first result is an obvious match (LinkedIn profile with all the details lining up), use it.
3. If ambiguous (multiple Mayas at Stripe, or you can't tell which), surface options to the user: "I found two possible matches — Maya Rodriguez (Design PM) and Maya Singh (Payments PM). Which one?" Don't guess.

Never enrich with someone else's data. Wrong enrichment is worse than no enrichment — it pollutes the CRM silently.

## Recipe 3: Company enrichment

Input: user mentions a company ("she works at Evalia") that isn't in the Companies DB.

If it's worth creating (user signaled tracking intent, or they're linking a person to it), enrich before creating:
1. Search the company website. Look for: industry, location, size, stage, founded date, tagline.
2. Search Crunchbase/LinkedIn for funding stage if it's a startup.
3. Check if it has a clear parent company (acquisition) or notable investors.

Create the Company record with what you found:
- `Name`, `Website`, `Industry` (multi-select — pick from canonical options), `Size`, `Stage`, `Founded`
- `HQ Location`: relation if the city is already in Places, else skip
- `Notes`: one-sentence description from the site's About page

Only enrich companies the user seems to actually care about. Every vendor and random mention doesn't need a page.

## Recipe 4: Pre-meeting briefing — fresh signal

Input: "brief me on Maya for coffee tomorrow."

The standard CRM briefing pulls everything the user has logged. The *deep* briefing layers recent public activity on top — things that changed since the last time they talked.

Steps (after the CRM briefing is assembled):
1. Search: `web_search("Maya Rodriguez Linear")` filtered to recent (last 30-60 days).
2. Check X / LinkedIn: recent posts, career changes, company news.
3. Look for: job change, new project launch, public talks, a substantive post, company funding news.

Report as a distinct "Fresh signal" section:

> **Fresh signal (from the web, past month):**
> - Posted a detailed thread on design tokens last week (twitter.com/...)
> - Linear raised a Series C on April 3 ($50M, Sequoia led)
> - Spoke at Config on "Ambient interfaces" April 15

Keep it to 3-5 items max, only things worth mentioning in conversation. Don't surface minor tweets or drama.

## Recipe 5: Filling gaps during weekly review

Input: user is working through the 📥 Inbox view and wants to bulk-enrich.

Strategy: for each person with thin data, do a quick enrichment pass (1-2 searches). Update in place. Keep a running tally — "enriched 8 people, 3 failed to match, 2 ambiguous."

Don't do this in parallel across 50 people — it's a lot of search volume and the user is going to review each one anyway. 5-10 at a time is sensible.

## Writing enrichment into the CRM

When you add enrichment data, **always attribute it.** Two places to put the note:

**In the properties:**
- `How we met`: "Found via Substack essay on mechanistic interpretability. Profile details enriched via LinkedIn, April 21, 2026."

**In the page body (more detail):**
```markdown
## Enrichment notes
- LinkedIn profile (fetched April 21, 2026): Researcher at DeepMind, based in London. Formerly at Google Brain (2020-2023).
- Topics: mechanistic interpretability, safety evals.
- Recent work: wrote "TransformerLens" library, active on Alignment Forum.
```

Distinguishing user-provided from enrichment-provided matters:
- If a fact turns out wrong, the user knows whether to blame memory or the web.
- During weekly review, the user can verify enriched facts specifically.
- It preserves provenance in case the CRM is ever audited or exported.

## Reporting back to the user

Always cleanly separate what came from the user vs. what came from enrichment:

> Added Neel Nanda to your radar.
>
> **From you:** Found via his Alignment Forum writing, interested in mechanistic interpretability.
>
> **From LinkedIn (enriched):** Researcher at DeepMind London. Prior: Google Brain. Active X account @NeelNanda5.
>
> Two things I couldn't verify: his specific team at DeepMind, and whether he's on X or only uses Substack. Let me know if you want me to dig further.

This transparency is non-negotiable. Never blur the line between "I know this because you told me" and "I found this on the web."

## Privacy guardrails — non-negotiable

1. **Professional-public only.** LinkedIn headline, X bio, company website, public talks, public GitHub — all fine. Home addresses, personal phone numbers, medical info, relationship status — never. If you stumble on private data in a search result, don't record it.

2. **No aggressive digging.** Two or three searches per person. If the public signal is thin, that's the signal. Don't paginate through archives looking for dirt.

3. **No cross-referencing unrelated identities.** If the user says "Alice at Stripe," don't also find her old reddit account and catalog it. Stay on-task.

4. **Respect explicit opt-outs.** If the user says "don't google her" or "I don't want web data for my family," honor it for the rest of the conversation and flag it for persistence in their `Thoughtfulness notes` if they want ("No web enrichment — user preference").

5. **Current events only on briefings.** A briefing should surface things that are relevant *now* — this month's signal. Don't surface a 5-year-old post out of context.

6. **When in doubt, ask.** "Want me to look her up, or do you have everything you need already?" is always the safe first move with personal contacts.

## Failure modes

**The name is too common.** "John" at "a startup" — you'll get nothing useful. Don't guess. Ask the user for one more clue (LinkedIn URL, full name, exact company) or skip enrichment.

**The person has minimal public footprint.** Many people aren't online in a findable way. Record that fact in the body note ("Minimal public footprint — no LinkedIn or X found") and move on. Don't pad the entry with weak guesses.

**Conflicting info.** LinkedIn says they work at Stripe, X bio says they work at Ramp. The more recent one usually wins — check post dates if possible. If you can't tell, record both with a note: "Conflicting company listings; user to verify."

**The right person, wrong facts.** Rare but possible — the LinkedIn profile is outdated. If the user reports a mismatch later, update and note the correction.

**MCP/search fails entirely.** Rate limit, outage, no results. Just tell the user: "Couldn't enrich right now — search didn't return anything. Want to fill in manually, or try again later?"
