# Note Schemas — Market Intelligence Vault

Complete frontmatter templates for each entity type. Copy the relevant block and fill in values. Use `null` for unknown fields (not empty string). Every note must have the `tags` array.

---

## Prospect (Target company / potential customer)

```yaml
---
name: "Company Name"
type: prospect
category: "ai-agent-platform | browser-agent | vertical-ai | saas-tool | dev-infra | crypto | legal-ai | finance-ai | sales-ai | other"
founded: YYYY
hq: "City, Country"
website: "https://example.com"

# Funding
funding_total: "$XM"
funding_last_round: "$XM Seed | Series A | etc"
funding_date: "Month YYYY"
investors:
  - "[[Investor Firm Name]]"
  - "[[VC Name]]"

# Team
founders:
  - "[[Founder Name]] (role)"
employees: "~XX"

# Scoring (required — never leave blank)
abadge_fit: "maximum | high | medium | low"
priority: "critical | high | medium | low"

# Research metadata
research_status: "complete | needs-update | stub"
last_researched: "YYYY-MM-DD"

tags:
  - credential-custody
  - agent-native
  - mcp-ecosystem
  # add domain-specific tags
---
```

### Prospect body structure

```markdown
## What they build
[1–2 sentence product description. No marketing fluff — what it actually does.]

## Customers
[Who uses it, estimated scale — users, ARR, employees, notable logos.]

## Why [[Your Product]] matters
[Specific mechanism. Not "they handle auth" — explain exactly what problem they have and how your product solves it. Be concrete.]

## Key people
- **[[Founder Name]]** — CEO. [Background: prior company, notable credential.] [@handle](https://twitter.com/handle)
- **[[Founder 2]]** — CTO. [Background.]

## Funding
- **Total**: $XM raised
- **Last round**: $XM [Round type], [Month YYYY], led by [[Investor]]
- **Notable investors**: [[Investor 1]], [[Investor 2]]

## Strategic signals
> [Most recent notable event — launch, partnership, funding, hiring — with date. This is what makes it urgent.]

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
category: "custodial | integration-platform | adjacent-identity | adjacent-auth | secrets-management | incumbent"
founded: YYYY
hq: "City, Country"
website: "https://example.com"
stage: "$XM raised, [round], [year] — brief status"

research_status: "complete | needs-update"
last_researched: "YYYY-MM-DD"

tags:
  - competitor
  # category-specific tags
---
```

### Competitor body structure

```markdown
## What they build
[Product description from a threat-assessment lens — what makes them a competitor.]

## Why they're a threat (Tier [X])
[Specific overlap with your product. What customers do they share? Where do they win?]

## Strengths
- [Key advantage 1]
- [Key advantage 2]

## Weaknesses / gaps
- [Where they fall short — and where you can win]

## Recent moves
> [Latest launch, pivot, funding, or acquisition — with date.]

## Key people
- **[[Founder/CEO]]** — [Background, relevant network.]
```

---

## Person (Founder, investor, influencer, advisor)

```yaml
---
name: "Full Name"
type: person
role: "Founder & CEO | Co-Founder & CTO | Investor | Advisor | Angel"
company: "[[Company Name]]"
twitter: "@handle"
linkedin: "https://linkedin.com/in/handle"
email: null  # only if publicly known
location: "City, Country"

# For investors only
firm: "[[Firm Name]]"
focus: "AI infrastructure, developer tools, fintech"
check_size: "$500K–$5M"

research_status: "complete | stub"

tags:
  - founder
  # or: investor, advisor, angel
---
```

### Person body structure

```markdown
## Background
[Prior companies, notable exits, education. What makes them credible/interesting.]

## Why they matter for [[Your Product]]
[Specific angle — are they a potential customer, channel partner, investor, advisor? What's the connection?]

## Notable work / signals
- [Publication, talk, open source project, notable hire, investment]
- [Any public statement relevant to your domain]

## Network
- Company: [[Company Name]]
- Key relationships: [[Person 2]], [[Person 3]]
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

# Partners relevant to your domain
key_partners:
  - "[[Partner Name]] — focus area"

# Portfolio companies in your space
relevant_portfolio:
  - "[[Company Name]]"

tags:
  - investor
  - seed-stage  # or: growth, crypto, enterprise
---
```

---

## ICP (Ideal Customer Profile)

```yaml
---
name: "T1 — AI Agent Platform Builder"  # Tier + descriptive name
type: icp
tier: "T1 | T2 | T3"
priority: "primary | secondary | tertiary"

# Who they are
role_titles: ["CTO", "VP Engineering", "Founder"]
company_stage: "Seed–Series B"
company_size: "5–50 employees"
domain: "AI agent infrastructure"

# The problem they have (this is your pitch entry point)
pain_point: "One-sentence description of their specific pain"
trigger_events:
  - "Raised Series A and need to productionize auth"
  - "Onboarding first enterprise customer who requires SOC 2"

# How to score prospects against this ICP
fit_signals:
  - "Manages credentials on behalf of end users"
  - "Exposes API that authenticates as users"
  - "Has MCP server with tool calls requiring auth"

tags:
  - icp
---
```

### ICP body structure

```markdown
## Who they are
[Archetype description — company type, team size, what they build, where they are in their journey.]

## Their pain (why they need you)
[Specific problem they have. Not "security" — what specifically breaks or burns them today without your product.]

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
topic: "market-signal | vertical-analysis | synthesis | competitor-move | fundraising-trend"
date: "YYYY-MM-DD"
tags:
  - intel
  - [topic-specific tag]
---
```

### Intel body structure

Free-form, but should include:
- Key finding or signal (bold, at top)
- Evidence / data points
- Implications for your product/strategy
- Companies affected (with wikilinks)
- Open questions

---

## Common frontmatter rules

1. **Use `null` for unknown fields** — not `""` or `"Unknown"` or `"TBD"`
2. **Dates as YYYY-MM-DD** for `last_researched`, as "Month YYYY" for funding dates
3. **Company names as wikilinks** when the note exists: `[[Company Name]]`
4. **Tags as a flat array** — no nested tags, use hyphens not spaces
5. **research_status** — always set: `complete` (thorough), `needs-update` (gaps known), `stub` (minimal info, placeholder)
