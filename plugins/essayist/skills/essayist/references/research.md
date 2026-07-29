# Research: the deep-dive playbook

The essays this skill emulates feel authoritative because they are outgunned on
evidence: a named company every ~100 words, numbers with dates and sources, history
that actually happened, objections researched rather than imagined. That density is
gathered, not written. Plan for research to take as long as drafting, often longer.

Scale the pipeline to the ask. A full piece from scratch runs all six passes. Improving
an existing draft runs Pass 0 plus verification of the claims already in it, adding new
research only where evidence is thin. Short pieces scale the bank targets down
linearly. For non-market genres (personal essays, cultural pieces, explainers), Passes
2–3 swap market hunting for the piece's own equivalents — primary texts, documentation,
archives, lived detail — and the verification rules stay exactly the same.

## Order of operations

### Pass 0 — Mine the user's own material first

Notion notes, transcripts, metrics, customer stories, prior drafts, things they've said
in the conversation. Proprietary evidence is the one thing no other writer has and the
strongest anti-generic signal a piece can carry ("the team at Mercor was kind enough to
provide…", a founder's own cohort data, a conversation recounted by name). Extract:
claims the user believes, numbers they own, stories they witnessed, people they can
quote. Flag which items need the user's confirmation before publishing (their metrics,
quotes attributed to real people).

### Pass 1 — Map the received wisdom

Search for what's currently being said about the topic: recent coverage, popular takes,
the consensus framing. The goal is to state the **default belief** precisely — the
essay needs an enemy, and it must be a belief people actually hold, not a strawman.
Capture 2–3 verbatim examples of the consensus (tweets, headlines, report claims) so
the piece can dramatize it concretely. If the planned thesis turns out to BE the
consensus, tell the user and dig for the sharper angle underneath.

### Pass 2 — Hunt the numbers

Market sizes (with ranges and years), growth rates, prices, adoption stats, labor data,
unit economics. Recipes:

- Market size: industry reports (Grand View, Gartner, IBISWorld summaries), then
  cross-check against a second source; report honest ranges ("$140–200B"), never a
  suspiciously precise single figure.
- Company metrics: press releases, funding announcements, earnings calls and filings,
  founder interviews and podcasts, credible reporting (Bloomberg, The Information).
- Comparisons that make numbers land: every stat needs a gloss in-sentence ("roughly
  300× two years earlier," "against the 6–18 months of a traditional rollout"). Hunt
  the comparison at research time, not draft time.
- Oddly specific beats round: "$12.99," "some date back to the 1940s," "~five people."
  When a source gives a precise figure, keep its precision.

### Pass 3 — Hunt the names

The genre names obscure companies, not just famous ones — obscurity signals insider
knowledge. Recipes: "[vertical] AI startup seed round [current year]," YC batch lists,
recent funding roundups, product launch coverage, "AI [industry] startups" lists from
credible newsletters. For each named company capture: what it does (one clause), one
metric or proof point with link, and why it fits the argument. Also collect **incumbent
foils** (the Thomson Reuters / Zendesk / legacy BPO of the space) and **people**:
founders (first names humanize), operators with quotable testimony, colleagues or known
thinkers whose lines can be cited by name.

### Pass 4 — Hunt the history

Every strong piece grounds its pattern in precedent: GPU/CPU for specialization, Roman
legions for hierarchy, Prussian General Staff, McCallum's org chart, Bobos in Paradise.
Search the history of the industry, prior technology transitions with the same shape,
and the canonical books/essays of the space. One well-told precedent beats three
name-dropped ones — capture enough detail to narrate it concretely (dates, people,
the vivid stake: "Train collisions were killing people").

### Pass 5 — Research the objection

Find the smartest version of the counterargument, not the weakest: what would a
skeptical practitioner say? What are incumbents actually doing (their AI announcements,
bookings, adoption claims — grant them their real evidence)? What data cuts against the
thesis? The objection beat only lands if the objection is real. If research surfaces a
counterargument the thesis can't survive, that's the most valuable finding possible —
bring it to the user with the stronger revised angle.

### Pass 6 — Verify

Before anything enters the draft: prefer primary sources (filings, official posts,
the original report) over aggregators; date every stat (a two-year-old market size
presented as current is a correctness bug — check whether the source has a newer
edition); when two sources conflict, take the conservative figure or give the range;
keep the URL for every load-bearing claim so it can be linked inline. Anything
unverifiable gets cut or explicitly softened to what IS known — never dressed up as
fact.

## The evidence bank

Maintain a working file (`evidence-bank.md`) while researching. One checkable fact per
STAT/FACT line — a compound entry ("$0.99/resolution, resolution rate 76%, $10/lead")
may not carry a single "verified"; split it, or mark confidence per fact. Facts added
later, during drafting or revision, enter the bank and get verified the same way before
they ship.

```
## [theme]
- CLAIM: what this supports
  STAT/FACT: one exact figure or fact, with date
  SOURCE: url (primary where possible)
  USE: where it might go (hook / evidence block / objection / close)
  CONFIDENCE: verified / single-source / needs-user-confirmation
```

Targets before outlining, scaled to a ~1,400-word piece (scale linearly, and halve the
entity targets for idea/vision-mode pieces):

- 20–30 named entities (companies, products, people) with one-line proof points
- 10–20 hard numbers with sources and glosses
- 1–2 historical precedents captured in narratable detail
- 2–3 verbatim consensus artifacts (the default belief, quotable)
- The smartest objection, with the incumbents' own evidence
- 2–3 candidate coined frames and 2–3 candidate callback images that emerged from
  the material

Gather roughly 2× what the piece will use. Density on the page comes from selecting
the best half, and the unused half is not waste — it's the next piece (surface leftover
angles to the user at delivery, in the notes file).

## Research tools

Use whatever the session provides, in rough priority: the user's connected sources
(Notion, files, transcripts) → web search with multiple parallel queries → full fetches
of the highest-value pages (primary sources, dense reports) → subagents for broad
sweeps when available (one per evidence pass, returning structured findings). For
fast-moving topics, constrain searches to the last 6–12 months and note publication
dates. Never rely on training-data memory for numbers, valuations, or who-runs-what —
those change; search instead.
