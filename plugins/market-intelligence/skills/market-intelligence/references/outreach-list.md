# Outreach List Reference

How to build, structure, rank, and export actionable outreach lists from vault intelligence.

---

## What makes an outreach list actually useful

A useful outreach list answers:
1. **Who** — real, verified people with active accounts
2. **Why them** — a specific reason this person is relevant
3. **Why now** — a recent signal that makes outreach timely
4. **How** — the platform and entry point (DM, email, comment, warm intro)
5. **What to say** — a specific opener, not a template

Lists without these are glorified address books.

---

## Contact data model

Each contact in an outreach list should carry:

```json
{
  "name": "Full Name",
  "role": "Co-Founder & CEO",
  "company": "Company Name",
  "section": "Category or segment label",

  "handles": {
    "twitter": "@handle",
    "twitter_url": "https://x.com/handle",
    "linkedin": "https://linkedin.com/in/handle",
    "github": "https://github.com/username",
    "email": null
  },

  "scoring": {
    "tier": "A | B | C | D",
    "priority": "critical | high | medium | low",
    "fit_score": "maximum | high | medium | low"
  },

  "outreach": {
    "angle": "One-sentence specific reason to reach out",
    "signal": "Recent thing they did/said that makes this timely",
    "type": "cold-dm | warm-intro | comment-first | email"
  },

  "verification": {
    "handle_verified": true,
    "verified_date": "YYYY-MM-DD",
    "verified_method": "browser | web-search | team-page"
  },

  "tags": ["founder", "ai-agent", "recently-funded"]
}
```

---

## Section structure

Group contacts into logical sections. Choose based on how the user will act on the list:

**By relationship to product:**
- Potential Customers (direct buyers)
- Ecosystem Partners (integration/distribution)
- Investors / Advisors
- Thought Leaders (amplification/influence)

**By company type** (good for product-led outreach):
- AI Infrastructure Founders
- Developer Tool Builders
- Open Source Maintainers
- Enterprise Buyers

**By urgency** (good for salespeople):
- Tier A — Reach out this week
- Tier B — This month
- Tier C — Warm up first

**By platform** (good for social-first outreach):
- Active on Twitter/X
- LinkedIn-first
- GitHub community

---

## Ranking contacts within a section

Sort by a combination of:
1. **Fit score** (maximum > high > medium > low)
2. **Recency of signal** (last 30 days outweighs last 6 months)
3. **Account activity** (active weekly poster > occasional > dormant)
4. **Relationship warmth** (mutual follows, interactions > cold)
5. **Response likelihood** (solo founders respond more than corporate spokespeople)

High-follower-count accounts are tempting but often less likely to respond to cold DMs. Founders of smaller funded companies (50–500 employees) often respond faster than famous thought leaders.

---

## Outreach angle — the most important field

The angle is what the person reads and decides whether to reply. It must be:
- **Specific**: tied to something they actually did, said, or built
- **Relevant**: connected to a real problem they have (not one you invented)
- **Brief**: one sentence, reads in 3 seconds
- **Non-salesy**: a genuine observation, question, or reaction

**Good angle examples:**
- "Saw you just shipped native MCP tool support — bet per-user credential routing is already on your backlog."
- "Your agent logs into Gmail and Salesforce as users — curious how you're handling per-user token isolation at scale."
- "Just read your thread on why env vars are terrible for production secrets — that's exactly the problem [Product] was built to replace."

**Bad angle examples:**
- "I'd love to connect and share some ideas."
- "Your company is doing amazing work in the AI space."
- "I think there's a lot of synergy between our products."

---

## HTML artifact structure

When generating an interactive HTML outreach tool, build with these components:

### Header
- Title: "Outreach: [Product/Campaign Name]"
- Subtitle: contact count, date generated
- Stats bar: total contacts, by section, by tier

### Controls
- **Search bar**: instant filter across name, company, role, tags, angle (JS, client-side)
- **Section tabs** or filter buttons: switch between sections or "All"
- **Tier filter**: A / B / C / D / All
- **Platform filter**: Twitter / LinkedIn / GitHub / All

### Contact card (per person)
```
[TIER A]  Name — Role at Company
[tag] [tag] [tag]
Handle: @handle  [↗ Open profile]
Angle: [the outreach angle]
Signal: [recent thing that makes this timely]
[📋 Copy handle]  [📝 Copy opener]   Status: [not-started ▾]
```

### Visual design
- Dark background (#0d1117 or similar) — easier on the eyes during extended use
- High-contrast text (#e6edf3)
- Tier badges color-coded: A=red (#f85149), B=orange (#f0883e), C=yellow (#d29922), D=grey (#6e7681)
- Monospace font for handles
- Hover states on cards (subtle border glow)
- Sticky header with search/filter controls
- Keyboard navigation (arrow keys to move between cards)

### Interaction patterns
- Click handle → opens profile in new tab
- "Copy handle" → copies `@handle` to clipboard
- "Copy opener" → copies pre-drafted DM opener (if angle is set)
- Status dropdown (not-started → reached-out → responded → converted)
- Export button → download current filtered view as CSV

---

## gen_outreach_html.py usage

The bundled script reads vault notes and generates HTML:

```bash
python3 scripts/gen_outreach_html.py \
  --vault-path /path/to/vault \
  --output /path/to/outreach.html \
  --title "Outreach: My Campaign" \
  --filter-tags "founder,investor"      # optional: only notes with these tags
  --filter-priority "critical,high"     # optional: only these priority levels
  --sections "Infrastructure,Investors" # optional: only these vault section names
```

Alternatively, build the HTML programmatically:
1. Read Person notes from `Market Landscape/People/`
2. Parse frontmatter (pyyaml or similar)
3. Apply filters, sort by priority/tier
4. Group into sections
5. Generate HTML using the structure and design spec above

---

## Quality checklist before exporting

Before handing any outreach list to a human for use:

- [ ] Every handle has been visually verified (not just web-searched)
- [ ] Every person's name matches their profile (not a different person)
- [ ] Every account has posts within the last 6 months
- [ ] Every contact has a specific outreach angle (not "great to connect")
- [ ] Tier A contacts all have a recent signal (last 30 days preferred)
- [ ] No duplicate contacts (same person in two sections)
- [ ] Contact count per section is actionable (5–20 per section; more is overwhelming)
- [ ] Sections make logical sense for how the user will act on them
