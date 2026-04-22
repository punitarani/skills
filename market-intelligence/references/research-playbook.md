# Research Playbook — Market Intelligence Vault

Step-by-step guidance for researching each entity type. Follow this for each note to reach "complete" research_status.

---

## Source priority

Use sources in this order (highest signal first):

1. **Company website** — product description, pricing, use cases, team page
2. **Crunchbase / LinkedIn** — funding rounds, team, headcount
3. **TechCrunch / The Information / Bloomberg** — funding announcements (always have round size + date + investors)
4. **GitHub** — open source repos reveal tech stack and community
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
- Cross-check: lead investor for each round, approximate date, total raised

**Extract**: all rounds (amount, type, date, lead investor), total raised to date

### Step 3 — Founders and team (5 min)
- Company team/about page
- LinkedIn: look up each founder for prior companies, education
- Twitter/X: do they tweet about their space? Find their handle
- GitHub: any notable OSS contributions?

**Extract**: founder names, roles, prior companies, LinkedIn URLs, Twitter handles

### Step 4 — The "why us" question (5 min) — most important
This is the hardest part and the most valuable. Force yourself to answer:
- Does this company handle credentials, auth tokens, or API keys on behalf of users?
- Do they log into external services AS their end users?
- Do they manage per-user or per-client isolated secrets?
- What breaks for them (security, compliance, scale) if they keep DIY-ing this?

Search: `"[Company Name]" OAuth | credentials | secrets | API keys | authentication`
Read their docs/API reference if publicly available.

**Write**: a specific "Why [[Your Product]] matters" section. Not generic. Not "they handle auth" — explain the exact mechanism.

### Step 5 — Recent signals (3 min)
- Twitter/X search: `from:[founder-handle] since:2024-01-01`
- Google: `"[Company Name]" after:2024-01-01`
- Product Hunt, GitHub releases, blog posts

**Extract**: most recent notable event (launch, partnership, funding, hiring surge) with date. This drives the priority score.

### Scoring guide
- **maximum fit**: They cannot operate at scale without solving the credentials problem. Their core product requires acting on behalf of users with stored credentials. 
- **high fit**: Credentials are a real pain point they've mentioned or hacked around. It's not their core product but it's a meaningful friction point.
- **medium fit**: They'll eventually need it as they grow, but have a working workaround today.
- **low fit**: Only relevant in edge cases or for one specific feature.

- **critical priority**: maximum or high fit + recent signal (funding round, product launch, enterprise customer announcement)
- **high priority**: maximum or high fit, no recent trigger — but the need is clear
- **medium priority**: medium fit or very early stage
- **low priority**: long-term watch

---

## Researching a Competitor

Goal: Understand them well enough to articulate the threat level and where you win.

### Step 1 — Positioning read (5 min)
- Read their website entirely: homepage, product, pricing, use cases, blog
- Look for: who they target, what problem they claim to solve, how they price
- Are they targeting the same customer as you? The same pain point?

### Step 2 — Funding and scale (3 min)
- Crunchbase, TechCrunch funding articles
- LinkedIn headcount (and growth trend if visible)
- Public ARR mentions (sometimes in investor announcements)

### Step 3 — Tech and product depth (5 min)
- GitHub if OSS — star count, contributors, recent commits
- Docs and API reference — what's the developer experience?
- Job postings — what are they building next? (check LinkedIn, Greenhouse, Lever)

### Step 4 — Tier classification
Assign tier honestly. Ask:
- Do they serve the same customers and solve the same problem? → Tier 1
- Could they expand into your space with one product addition? → Tier 1.5
- Do they serve the same buyer but for a different problem? → Tier 2
- Are they legacy/slow-moving but established? → Tier 3

### Step 5 — Strengths and gaps
Write these from a competitive battlecard lens:
- Where do they win? (distribution, price, brand, features)
- Where do you win? (agent-native, per-profile isolation, audit trail, delivery modes)

---

## Researching a Person

Goal: Know enough to have an informed first conversation or to understand their relevance to the space.

### Step 1 — LinkedIn (3 min)
- Prior companies (especially exits or notable roles)
- Education (common for deep-tech founders)
- Current company and title

### Step 2 — Twitter/X (2 min)
- Do they tweet about your domain? What's their POV?
- Recent posts reveal what they're thinking about right now

### Step 3 — Public contributions (2 min)
- GitHub (especially for technical founders)
- Published papers, talks, podcasts
- Blog posts or newsletters

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
4. Which partners are active in AI/infrastructure? (name the right person)

### Sources
- Firm website — partners, portfolio, thesis statement
- Partner Twitter/X — what they talk about reveals actual thesis
- Crunchbase — full portfolio, typical check size
- LinkedIn — partner backgrounds (ex-founder vs. banker backgrounds matter)
- Their recent fund announcements (size signals how much dry powder)

---

## Research anti-patterns to avoid

- **Copying press release language**: "X is revolutionizing Y" tells you nothing. Rewrite in plain terms.
- **Ignoring the docs**: For developer tools, the API docs reveal more about the product than the homepage.
- **Treating funding as a proxy for fit**: A well-funded company can still be a bad prospect. Score on need, not raise size.
- **Leaving research_status blank**: Always set it. `stub` is fine — it tells future researchers where to pick up.
- **Creating duplicate notes**: Always search the vault before creating a new person or investor note.
- **Stale signals**: A 2022 product launch is not a "recent signal". Only include things that are within 12 months unless historically significant.
