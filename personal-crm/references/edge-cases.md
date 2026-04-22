# Personal CRM — Edge cases and gotchas

Failure modes, ambiguous requests, and the subtle decisions that keep the CRM clean.

## Discovery failures

**Search for "Personal CRM" returns nothing.** The user may have renamed the page. Ask them for the URL directly: *"I couldn't find a page called 'Personal CRM' in your workspace. What's the URL of your CRM dashboard?"*

**Search returns multiple matches.** Teamspaces or templates can produce duplicates. Show the user each match with enough context to pick (title + parent path if available): *"I found two pages named 'Personal CRM' — one in your private workspace, one in the Team teamspace. Which one?"*

**The fetched page doesn't have 5 `<database>` tags.** The user's CRM structure diverges from the canonical build. Fall back to discovering each database individually: *"I found your CRM page but the structure looks different from what I expected. Can you share the URLs of your People and Interactions databases at minimum?"* You can operate with a subset if you have to, but flag the limitation.

## Name collisions: multiple people with the same first name

The user will often say "Alice" when there are 3 Alices. Don't guess — ask.

```
notion-search returns:
1. Alice Chen (Tier: Inner 5, Anthropic)
2. Alice Park (Tier: Network 50, Stripe)
3. Alice Smith (Status: Never met - on radar)

Ask: "Which Alice? Chen at Anthropic, Park at Stripe, or Smith (from your radar list)?"
```

If the user's context is obvious (e.g. they said "my coffee with Alice at Anthropic"), pick the match and confirm by name + disambiguator in your response, not silently.

## "Add her to my inner circle" for someone never met

Don't elevate Tier past `Extended 150` for someone whose Status is `Never met - on radar`. Tiers are about relationship depth; you can't have deep relationships with people you've never met. If the user insists, do it — but flag it: "Setting Tier to Inner 5 even though Status is Never met - on radar. Consider adding an Interaction or updating Status first so the system works correctly."

## Target page doesn't exist for a relation

When the user says "Alice works at Anthropic" and Anthropic isn't in Companies yet, you have three options:

1. **Create Anthropic first**, capture its URL, then set the relation. Best when the user's request implies the company matters to track.
2. **Skip the relation**, put "ML engineer at Anthropic" in `Current role` text. Fastest. Appropriate when the user is focused on the person, not the company.
3. **Ask**. When genuinely unclear.

Default to option 2 for capture speed unless the user mentioned the company as a tracking target.

## Updates vs creates — choosing right

Always `notion-search` for existing records before creating. But sometimes the right call is still to create — for example, if the user says "add another Alice I just met" even when an Alice exists. Trust the user's framing but confirm on ambiguity.

Heuristic: if the user uses the word "add" → creating is likely. If they use "update", "change", or "her email is...", searching first is required. If they say "log" → refers to an Interaction (new row), not an update to the person.

## When a person changes company

The user says "Bob left Stripe and joined OpenAI." This is a simple update — point `Current company` to the OpenAI page (create OpenAI if missing) and update `Current role` to the new title.

**Note:** the canonical schema doesn't track career history natively. If the user wants "Bob worked at Stripe 2020–2025, now at OpenAI" preserved, a Roles junction database would be needed (not part of this skill). Either tell the user the old company info will be overwritten, or log an Interaction with a summary like "Bob announced he's leaving Stripe for OpenAI" so the history lives in the interaction log.

## "People" vs "Mentioned" — the single most important Interactions distinction

- **People** = attendees physically present at the interaction
- **Mentioned** = people who came up in conversation but were NOT there

This matters because **the `Last interaction` rollup only fires for People, not Mentioned.** If you put Bob (who the user just talked about with Alice) in the `People` field, Bob's follow-up clock resets — which is wrong, they didn't actually talk.

Example: "Had coffee with Alice, she mentioned her cofounder Bob a lot."
- People: [Alice]
- Mentioned: [Bob]

Not:
- People: [Alice, Bob] ❌ (Bob wasn't there)

Getting this right is the difference between a working cadence system and a broken one.

## Interactions spanning multiple people: one row or many?

**One row** for a group conversation — a dinner with 4 people is one Interaction with 4 entries in `People`. The Last interaction rollup fires for all 4.

**Separate rows** when the conversations were substantively different — e.g., you had coffee with Alice, then a separate call with Bob the same day. Create two Interactions.

When in doubt: one row. Easier to merge mentally than to split retroactively.

## Setting a self-relation: which side?

Self-relations may be one-way or two-way depending on the user's setup. In the default canonical build they are one-way — setting Bob as Alice's `Introduced by` does NOT automatically set Alice on Bob's profile. If the user wants symmetry, either:

1. **Set both sides explicitly.** Update Alice's `Introduced by` with Bob, and update Bob with a reverse reference in whatever appropriate field (often `Introduced by` or `Should meet` — there's no "Introduced me to" field in the canonical schema).
2. **Tell the user** they can enable two-way sync in the Notion UI (property settings → Show on People → name reverse) if they want this permanently.

In practice: setting one direction is usually enough. The user can browse either side via filter.

## "Delete this person" / "remove this contact"

Notion's API supports deletion via `in_trash: true` on update. For a skill that mostly *adds* and *queries*, deletion is a rare request — treat it carefully.

1. Confirm with the user before deleting. "You want me to delete Alice Chen from the CRM entirely? This also removes her from any Interactions that referenced her."
2. Offer a softer option: set `Status: "Do not contact"` which keeps the record but flags it. This preserves Interaction history.

If they confirm delete, use `notion-update-page` with `in_trash: true`. But prefer soft-delete.

## Duplicate people: the user created two rows for the same person

Happens. "Alice Chen" and "Alice J. Chen" might be the same person. If the user reports this, you can't merge in one step — Notion doesn't have a merge API. The workflow is:

1. Pick the keeper (usually the one with more data).
2. Re-point every Interaction that references the duplicate to the keeper.
3. Copy any unique properties from the duplicate to the keeper.
4. Trash the duplicate.

This is multi-step and error-prone. Tell the user the steps and ask whether to proceed or let them merge in the UI. The UI is often faster for this.

## Birthday already populated — don't overwrite

If a person has a Birthday set and the user gives a different date, confirm before overwriting. Birthdays can be wrong in both directions; a silent overwrite loses information.

## The "Topics" field on People vs on Interactions

- **People.Topics** = what this person cares about or is expert in. Persistent.
- **Interactions.Topics discussed** = what came up in this specific conversation. Event-specific.

When the user says "Alice is into mechanistic interpretability," that's a People.Topics. When they say "We talked about interp at coffee," that's Interactions.Topics discussed. Often both apply — it's fine to set both. Creating the Topic once covers both relations.

## Creating a Topic on the fly

Topics fill organically. When the user mentions a topic you don't see in the DB, quickly create it with just Name and Category. Don't agonize over categorization — `Professional` is the safe default for work topics, `Personal` for hobbies/interests. The user can refine later.

## "Alice is visiting SF next week" — how to capture?

This is a Note, not a Property. The CRM has no "visiting dates" field. Three options:

1. Append to Alice's page body: "Visiting SF May 1-5, 2026" — good for transient info.
2. Create a Next follow-up date pointing at her arrival — triggers a reminder.
3. Pre-create an Interaction for the planned meetup ("Lunch with Alice on May 3, SF") — converts to an actual logged interaction when it happens.

Option 2 is probably best. Confirm with the user.

## Working hours / timezone

All dates use ISO format without timezone (Notion stores as local date). Don't attempt timezone conversion — use the date as given. For datetimes with specific times, use UTC (`Z`) or the user's local time consistently.

## When the formula doesn't seem to update

The `Last interaction` rollup and dependent formulas update after Notion re-computes — usually immediately, sometimes with a few seconds of lag. If the user says "I just logged an interaction but Follow-up urgency still says Overdue," suggest a refresh; the numbers will catch up.

## Tier changes — when and how to suggest

The user rarely asks for tier changes out of the blue. Suggestions come from patterns you notice:

- If someone hasn't been contacted in 2+ cadence-periods, the right suggestion is often to DEMOTE tier rather than mark as Dormant. "Bob hasn't been contacted in 6 months and his tier is Close 15 — consider moving to Network 50 or Extended 150 so his overdue flag isn't constantly triggering."
- If someone is in Extended 150 but the user is initiating most contact and conversations are substantive, the right suggestion is to PROMOTE.

Surface these observations during quarterly audits, not on every interaction log.

## Adding contact info that's already there

If the user says "add Alice's LinkedIn: ..." and Alice already has a LinkedIn URL set, compare. If the same, noop (tell the user it's already there). If different, confirm before overwriting.

## Tool failures: what to do

If `notion-create-pages` returns an error:

- **"validation_error" with "Type error"** — usually a property value doesn't match the schema. Check: is a date missing its `is_datetime` key? Is a select option value exactly matching the allowed list? Is a relation a stringified JSON array?
- **"not_found"** — the parent or referenced page doesn't exist. Verify the data source ID wasn't copied with a typo. Re-run discovery if needed.
- **Silent failures where a field just isn't set** — you probably tried to set a read-only field (rollup, formula, timestamp). Check the schema reference.
- **"property not found"** — the user's schema may have been modified. Fetch the data source with `notion-fetch` using `collection://<DS_ID>` to see the current property list and adapt.

Always report errors to the user honestly. Don't pretend a failed write succeeded.
