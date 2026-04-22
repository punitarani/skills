# Research Playbook — Market Intelligence Vault

Step-by-step guidance for researching each entity type. Follow this for each note to reach "complete" research_status.

---

## Source priority

Use sources in this order (highest signal first):

1. **Company website** — product description, pricing, use cases, team page (most reliable for social handles)
2. **Crunchbase / LinkedIn** — funding rounds, team, headcount
3. **TechCrunch / The Information / Bloomberg** — funding announcements (have round size + date + investors)
4. **GitHub** — open source repos reveal tech stack; founder bios often list Twitter handle
5. **Twitter/X** — founder posts signal product direction, recent launches, hiring
6. **YC Directory (ycombinator.com/companies)** — for YC companies: batch, description, founders
7. **Product Hunt** — launch details, initial reception, customer comments
8. **LinkedIn company page** — headcount, recent hires, job postings
9. **Pitchbook / Apollo** — for detailed funding data (if available)

Always look for **dated evidence** — a funding article from 2 years ago tells you less than a tweet from last week.

---

## Researching a Prospect

Goal: Understand them well enough to write a specific, compelling pitch and score them accurately.

### Step 1 — Find the basics (5 min)
- Search: `"[Company Name]" site:techcrunch.com OR site:crunchbase.com`
- Visit their website — read the homepage, pricing page, and "How it works"
- Check YC directory if they might be YC-backed

**Extract**: founding year, HQ, website, product description, customer type

### Step 2 — Funding deep dive (3 min)
- Search: `"[Company Name]" funding raised site:techcrunch.com`
- Crunchbase profile for full round history

**Extract**: all rounds (amount, type, date, lead investor), total raised to date

### Step 3 — Founders and team (5 min)
- Company team/about page — **the most reliable source for social handles**
- LinkedIn: each founder's prior companies, education
- GitHub: founder bio often lists Twitter handle; any notable OSS?

**Extract**: founder names, roles, prior companies, LinkedIn URLs, Twitter handles

### Step 4 — The "why us" question (5 min) — most important
Force yourself to answer:
- Does this company handle credentials, tokens, or API keys on behalf of users?
- Do they log into external services AS their end users?
- What breaks for them (security, compliance, scale) if they keep DIY-ing this?
- Read their docs/API reference if publicly available

**Write**: a specific "Why [[Your Product]] matters" section. Explain the exact mechanism, not "they handle auth."

### Step 5 — Recent signals (3 min)
- Twitter/X: `from:[founder-handle] since:2024-01-01`
- Google: `"[Company Name]" after:2024-01-01`
- Product Hunt, GitHub releases, blog posts

**Extract**: most recent notable event (launch, partnership, funding, hiring) with date. This drives priority score.

### Scoring guide
- **maximum fit**: Core to business model. Cannot operate at scale without solving the problem.
- **high fit**: Real pain point they've mentioned or hacked around. Meaningful friction.
- **medium fit**: Will eventually need it, but have a working workaround today.
- **low fit**: Only relevant in edge cases.

- **critical priority**: max/high fit + recent signal (funding, product launch, enterprise customer)
- **high priority**: max/high fit, no recent trigger — but need is clear
- **medium priority**: medium fit or very early stage
- **low priority**: long-term watch

---

## Researching a Competitor

Goal: Understand them well enough to articulate threat level and where you win.

### Step 1 — Positioning read (5 min)
- Read their website entirely: homepage, product, pricing, use cases, blog
- Who do they target? What problem do they claim to solve?

### Step 2 — Funding and scale (3 min)
- Crunchbase, TechCrunch funding articles
- LinkedIn headcount trend
- Public ARR mentions

### Step 3 — Tech and product depth (5 min)
- GitHub if OSS — star count, contributors, recent commits
- Docs and API reference — what's the developer experience?
- Job postings — what are they building next?

### Step 4 — Tier classification
- Same customers, same problem → Tier 1
- Could expand into your space with one addition → Tier 1.5
- Same buyer, different problem → Tier 2
- Legacy/slow-moving but established → Tier 3

### Step 5 — Strengths and gaps
From a competitive battlecard lens:
- Where do they win? (distribution, price, brand, features)
- Where do you win? (differentiation, architecture, target segment)

---

## Researching a Person

Goal: Know enough to have an informed first conversation and reach out on the right platform with the right message.

### Step 1 — LinkedIn (3 min)
- Prior companies (especially exits or notable roles)
- Current company and title

### Step 2 — Twitter/X (2 min)
- Find their handle — start with **company team page**, then GitHub bio, then search
- Do they tweet about your domain? What's their POV?
- Recent posts reveal what they're thinking about right now

### Step 3 — Public contributions (2 min)
- GitHub (especially for technical founders) — repos, recent commits
- Published papers, talks, podcasts, newsletters

### Step 4 — Verify the handle (required before outreach)
**Do not skip this.** Navigate to their actual profile and confirm:
- Name on profile matches the person you researched
- Bio/current role matches expected company
- Account has recent activity and credible follower count

Read `references/social-verification.md` for the full verification workflow and common failure patterns (fabricated names, wrong person, stale handles).

Set `handle_verified: true` + `handle_verified_date` in the frontmatter only after this check.

### Step 5 — Craft the outreach angle
Every person note should include a specific outreach angle — one sentence tied to something they said or did publicly.

Good: "Just read your thread on agent identity — the comment about env vars being a terrible security model is exactly the problem [Product] solves."
Bad: "Your work in AI is really interesting and I'd love to connect."

**The "why they matter" question**: Are they a potential:
- **Buyer/champion** at a prospect company?
- **Influencer** who shapes what their peers buy?
- **Investor** whose portfolio overlaps with your ICP?
- **Advisor** with deep domain expertise?
- **Partner** for distribution or integration?

---

## Researching an Investor

Goal: Understand their thesis and portfolio to assess fit and find warm introductions.

### Key questions
1. What stage do they lead? (Seed, Series A, growth)
2. What's their stated or revealed thesis in your domain?
3. Which portfolio companies overlap with your ICP? (potential warm intros)
4. Which partners are active in your space? (name the right person)

### Sources
- Firm website — partners, portfolio, thesis statement
- Partner Twitter/X — what they talk about reveals actual thesis
- Crunchbase — full portfolio, typical check size
- LinkedIn — partner backgrounds (ex-founder vs. banker backgrounds matter)

---

## Research anti-patterns to avoid

- **Copying press release language**: "X is revolutionizing Y" tells you nothing. Rewrite in plain terms.
- **Ignoring the docs**: For developer tools, the API docs reveal more about the product than the homepage.
- **Treating funding as a proxy for fit**: Well-funded ≠ good prospect. Score on need, not raise size.
- **Leaving research_status blank**: Always set it. `stub` is fine — it tells future researchers where to pick up.
- **Creating duplicate notes**: Always search the vault before creating a new person or investor note.
- **Stale signals**: A 2022 product launch is not a "recent signal". Only include things within 12 months.
- **Unverified handles**: Never export a contact for outreach without navigating to their profile. See `references/social-verification.md`.
- **Trusting AI-generated names**: When research was generated quickly at scale, verify that named founders actually exist at that company. Check the real team page. Fabricated names are common in auto-generated research.
