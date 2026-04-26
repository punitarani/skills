# Social Verification Reference

How to verify that social handles are real, active, and belong to the right person — before any outreach goes out.

This matters more than most researchers expect. Fabricated or stale handles are common when research is generated quickly at scale. A wrong DM is worse than no DM — it signals you haven't done your homework and poisons the relationship before it starts.

---

## The core rule

**Never trust a handle you haven't visually confirmed at the actual profile URL.**

Web search results, company blog posts, and AI-generated research can all have wrong handles. The only source of truth is the live profile page.

---

## Platform verification guide

### Twitter / X

**Profile URL pattern**: `https://x.com/{handle}`

**Navigate and confirm**:
- Displayed name matches expected contact
- Bio or pinned post mentions expected company or role
- Follower count is credible (see thresholds below)
- Account has posts within the last 3–6 months

**Red flags**:
- Name on profile is a different person entirely
- Bio is unrelated (sports fan, different country, different industry)
- Follower count under 50 with no bio — likely wrong or abandoned
- "This account doesn't exist" → handle is wrong or suspended
- Private account with 0 visible posts — exists but can't verify content

**Handle patterns that tend to be wrong**:
- Handles with trailing numbers (`@jsmith12`) — often not the founder
- Handles that are first+last with no company context — common name collision
- Handles found via a Google search snippet, not from the person's own profile

**Follower count heuristics**:
| Type | Expected range |
|------|----------------|
| Founder at funded startup | 200–10,000+ |
| Developer advocate / thought leader | 1,000–50,000+ |
| VC partner | 1,000–20,000+ |
| Technical founder (less social) | 100–2,000 |
| < 50 followers, no bio | Almost certainly wrong or abandoned |

---

### LinkedIn

**Profile URL pattern**: `https://linkedin.com/in/{slug}`

**Navigate and confirm**:
- Displayed name matches
- Current role and company match
- Profile photo present (not placeholder)

**Note**: LinkedIn often requires login to see full profiles. If blocked, use the company website team page or Google: `"[Full Name]" "[Company]" site:linkedin.com`.

---

### GitHub

**Profile URL pattern**: `https://github.com/{username}`

**Navigate and confirm**:
- Display name matches
- Bio or pinned repos relate to expected domain
- Recent commit activity
- Company field populated

GitHub handles are often more reliable than Twitter handles — developers tend to use their GitHub username consistently across platforms, and GitHub profiles are less likely to be impersonated.

---

## Finding correct handles when a profile is wrong

Work through these steps in order:

**Step 1 — Company team page**
Most startups list founders on `/team`, `/about`, or `/company`. Look for social links directly. This is the highest-trust source.

**Step 2 — Web search**
```
"[Full Name]" "[Company Name]" Twitter
"[Full Name]" "[Company Name]" site:x.com
```
Look for profile links in results, not just text mentions.

**Step 3 — LinkedIn → Twitter cross-reference**
Find the person on LinkedIn → check their contact info or recent posts for a Twitter/X mention.

**Step 4 — GitHub profile**
Many developers list their Twitter handle in their GitHub bio. Search GitHub for their name or find them via the company's GitHub org.

**Step 5 — Product Hunt / YC directory**
YC founders often list handles on the YC company page. Product Hunt profiles link to social accounts.

**Step 6 — Cross-reference from mutual contacts**
Look for retweets, mentions, or "reply" threads involving known contacts at the same company. Founders often interact with each other publicly.

---

## Handling "this person doesn't exist"

If a person in the vault has no verifiable social presence:

1. Check if the company is real and confirm actual founders (Crunchbase, company website)
2. If the vault note has wrong founders (common in AI-generated research), replace with real ones
3. Write corrected note: update name, role, handle, `research_status: complete`
4. Note the replacement in the body: `> Previously listed as [wrong name]. Corrected [date].`

When replacing a person entirely:
- The replacement should serve the same strategic purpose (same tier, same angle)
- Prefer active accounts (last post within 3 months)
- A real person with 500 followers who is active beats a famous person who hasn't posted in 2 years

---

## Batch verification workflow

For lists of 20+ contacts, use parallel subagents — each handling 5–10 contacts:

```
Agent prompt:
Verify these [N] Twitter/X handles. For each:
1. Navigate to https://x.com/{handle}
2. Read: displayed name, bio, follower count, most recent post date
3. Classify: VERIFIED | LOW-CONFIDENCE | WRONG-PERSON | INACTIVE | DOESNT-EXIST
4. For WRONG/INACTIVE/MISSING: search for the correct handle
5. Return a JSON report:
   [{name, company, handle_checked, status, corrected_handle, notes}]

Contacts to check:
[list]
```

Spawn all agents in one message. Aggregate their JSON reports into the verification summary.

---

## Verification status taxonomy

Update Person note frontmatter fields after verification:

| Status | Field values | When to use |
|--------|-------------|-------------|
| Confirmed good | `handle_verified: true`, `method: browser` | Navigated to profile, name + bio match |
| Found via search | `handle_verified: true`, `method: web-search` | Found via search + profile confirmed |
| From team page | `handle_verified: true`, `method: team-page` | Directly from official company source |
| Unconfirmed | `handle_verified: false` | Not yet checked |
| Not found | `twitter: null`, `handle_verified: false` | Searched and couldn't find any handle |

---

## Common failure patterns

**1. Plausible but wrong person**
`@jaredsmith` is taken by a random person, not the founder you want. Profile name matches the first name but bio is completely different. Fix: search `"[Full Name]" "[Exact Company]" Twitter`.

**2. Fabricated person entirely**
The name doesn't correspond to anyone at the company. This is surprisingly common in auto-generated research. Fix: always check the actual company team page and cross-reference with Crunchbase founders list.

**3. Real person, stale handle**
The person changed their handle. Old one now 404s or belongs to someone new. Fix: search their current LinkedIn profile for Twitter link, or search their name.

**4. Very low follower count**
Handle exists, name matches, but 3 followers and 2 posts. They created the account and never used it. Fix: update the note with this context. They may be more active on LinkedIn. Don't include in outreach list unless LinkedIn path is available.

**5. Private account**
Can't see bio or posts. Risk is low if name matches, but you can't DM without a follow acceptance. Fix: mark `handle_verified: true` (name match) but note the account is private; use LinkedIn for outreach instead.

**6. Name collision with unrelated person**
Two people named "Chris Johnson" — one is the developer you want, one is a sports journalist with the same handle. Fix: always confirm company or domain in the bio, not just the name.
