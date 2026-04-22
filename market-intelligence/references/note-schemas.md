# Note Schemas — Market Intelligence Vault

Complete frontmatter templates for each entity type. Copy the relevant block and fill in values. Use `null` for unknown fields (not empty string). Every note must have the `tags` array.

The `fit_score` field is generic — rename it to match your domain if preferred (e.g., `relevance`, `need_score`). The values (maximum/high/medium/low) stay consistent.

---

## Prospect (Target company / potential customer)

```yaml
---
name: "Company Name"
type: prospect
category: "ai-agent-platform | browser-agent | vertical-ai | saas-tool | dev-infra | fintech | legal-tech | other"
founded: YYYY
hq: "City, Country"
website: "https://example.com"

# Funding
funding_total: "$XM"
funding_last_round: "$XM Seed | Series A | etc"
funding_date: "Month YYYY"
investors:
  - "[[Investor Firm Name]]"

# Team
founders:
  - "[[Founder Name]] (role)"
employees: "~XX"

# Scoring (required — never leave blank)
fit_score: "maximum | high | medium | low"
priority: "critical | high | medium | low"

# Research metadata
research_status: "complete | needs-update | stub"
last_researched: "YYYY-MM-DD"

tags:
  - domain-tag
  - signal-tag
---
```

### Prospect body structure

```markdown
## What they build
[1–2 sentence product description. No marketing fluff — what it actually does.]

## Customers
[Who uses it, estimated scale — users, ARR, employees, notable logos.]

## Why [[Your Product]] matters
[Specific mechanism. Explain exactly what problem they have and how your product solves it. Be concrete — not "they handle auth" but "they store OAuth tokens for 10k users and have no per-user isolation".]

## Key people
- **[[Founder Name]]** — CEO. [Background: prior company, notable credential.] [@handle](https://x.com/handle)
- **[[Founder 2]]** — CTO. [Background.]

## Funding
- **Total**: $XM raised
- **Last round**: $XM [Round type], [Month YYYY], led by [[Investor]]
- **Notable investors**: [[Investor 1]], [[Investor 2]]

## Strategic signals
> [Most recent notable event — launch, partnership, funding, hiring — with date. This is what makes outreach timely.]

## Open questions
- [What you couldn't find or need to verify]
```

---

## Competitor (Competing or adjacent company)

```yaml
---
name: "Company Name"
type: competitor
tier: "1 | 1.5 | 2 | 3"
category: "direct | integration-platform | adjacent | incumbent | open-source"
founded: YYYY
hq: "City, Country"
website: "https://example.com"
stage: "$XM raised, [round], [year] — brief status"

research_status: "complete | needs-update"
last_researched: "YYYY-MM-DD"

tags:
  - competitor
---
```

### Competitor body structure

```markdown
## What they build
[Product description from a threat-assessment lens.]

## Why they're a threat (Tier [X])
[Specific overlap. What customers do they share? Where do they win? Where do you win?]

## Strengths
- [Key advantage 1]

## Weaknesses / gaps
- [Where they fall short]

## Recent moves
> [Latest launch, pivot, funding, or acquisition — with date.]

## Key people
- **[[Founder/CEO]]** — [Background, relevant network.] [@handle](https://x.com/handle)
```

---

## Person (Founder, investor, influencer, advisor)

```yaml
---
name: "Full Name"
type: person
role: "Founder & CEO | Co-Founder & CTO | Investor | Advisor | Angel | Developer Advocate"
company: "[[Company Name]]"

# Social handles — always verify before outreach
twitter: "@handle"
twitter_url: "https://x.com/handle"
linkedin: "https://linkedin.com/in/handle"
github: "https://github.com/username"
email: null  # only if publicly known

# Verification (required fields)
handle_verified: false  # set true only after visual profile confirmation
handle_verified_date: null
handle_verified_method: null  # browser | web-search | team-page | direct

# Outreach tracking
outreach_status: "not-started | reached-out | responded | converted | not-a-fit"
outreach_tier: "A | B | C | D"
last_contact: null

location: "City, Country"

# For investors only
firm: "[[Firm Name]]"
focus: "AI infrastructure, developer tools"
check_size: "$500K–$5M"

research_status: "complete | stub"
last_researched: "YYYY-MM-DD"

tags:
  - founder  # or: investor, advisor, angel, developer-advocate, thought-leader
  - handle-unverified  # change to handle-verified after verification
---
```

### Person body structure

```markdown
## Background
[Prior companies, notable exits, education. What makes them credible/interesting in this space.]

## Why they matter for [[Your Product]]
[Specific angle — are they a potential customer, channel partner, investor, advisor? What's the connection?]

## Public signals
- [Recent tweet, blog post, talk, launch — with date]
- [GitHub repos, OSS contributions, newsletters]

## Outreach angle
> [One sentence specific to this person. Ties to something they said or did publicly. Never generic.]

## Network
- Company: [[Company Name]]
- Key relationships: [[Person 2]], [[Person 3]]
- Investors: [[Fund Name]]
```

---

## Investor (VC firm or angel fund)

```yaml
---
name: "Firm Name"
type: investor
website: "https://example.com"
hq: "City, Country"
aum: "$XB"
stage_focus: "Seed | Series A–B | Growth"
check_size: "$X–$XM"
thesis: "Brief investment thesis (1 sentence)"

key_partners:
  - "[[Partner Name]] — focus area"

relevant_portfolio:
  - "[[Company Name]]"

research_status: "complete | needs-update"
last_researched: "YYYY-MM-DD"

tags:
  - investor
  - seed-stage  # or: growth, enterprise, ai-focused
---
```

---

## ICP (Ideal Customer Profile)

```yaml
---
name: "T1 — Descriptive ICP Name"
type: icp
tier: "T1 | T2 | T3"
priority: "primary | secondary | tertiary"

role_titles: ["CTO", "VP Engineering", "Founder"]
company_stage: "Seed–Series B"
company_size: "5–50 employees"
domain: "Brief domain description"

pain_point: "One-sentence specific pain"
trigger_events:
  - "Raised Series A and now faces [specific problem]"
  - "Onboarding first enterprise customer who requires [X]"

fit_signals:
  - "Observable signal that indicates this ICP fit"
  - "Another signal"

tags:
  - icp
---
```

### ICP body structure

```markdown
## Who they are
[Archetype — company type, team size, what they build, where they are in their journey.]

## Their pain (why they need you)
[Specific problem. Not "security" — what specifically breaks or costs them today without your product.]

## How to find them
- YC batches with these characteristics: [...]
- Job postings mentioning: [...]
- GitHub repos with patterns like: [...]
- Communities they hang out in: [...]

## Pitch frame
> "[One-sentence opener that speaks to their specific pain]"

## Example companies
- [[Company A]] — [why they fit]
- [[Company B]] — [why they fit]
```

---

## Intel (Thematic research note)

```yaml
---
name: "Note title"
type: intel
topic: "market-signal | vertical-analysis | synthesis | competitor-move | fundraising-trend | relationship-map | verification-report"
date: "YYYY-MM-DD"
tags:
  - intel
  - [topic-specific tag]
---
```

Intel notes are free-form but should include: key finding (bold, at top), evidence/data points, implications, companies affected (wikilinked), open questions.

---

## Common frontmatter rules

1. **Use `null` for unknown fields** — not `""` or `"Unknown"` or `"TBD"`
2. **Dates as YYYY-MM-DD** for `last_researched`/`handle_verified_date`, "Month YYYY" for funding dates
3. **Company names as wikilinks** when the note exists: `[[Company Name]]`
4. **Tags as a flat array** — no nested tags, use hyphens not spaces
5. **research_status** — always set: `complete`, `needs-update`, or `stub`
6. **handle_verified** — always set on Person notes. `true` only after visual profile confirmation.
