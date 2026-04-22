# Personal CRM — Schema reference

Authoritative field list for all 5 databases in the canonical Personal CRM build. Read this when you need to confirm a select option, a property name, or a relation direction.

**Note on IDs.** This file describes the *canonical schema*. The actual data source IDs and database URLs are specific to each user's workspace — you discover them at the start of the conversation (see SKILL.md → "Before doing anything" → Step 2) and hold them in working memory. Throughout this file, placeholders like `<PEOPLE_DS_ID>` refer to those discovered values.

## People database

Referenced as `<PEOPLE_DS_ID>` and `<PEOPLE_DB_URL>` in examples.

### Writable properties

| Property | Type | Options / notes |
|---|---|---|
| `Name` | Title | Full name, format "First Last" |
| `Status` | Select | `Never met - on radar`, `Met once`, `Active`, `Dormant`, `Lost touch`, `Do not contact` |
| `Tier` | Select | `Inner 5`, `Close 15`, `Network 50`, `Extended 150`, `Periphery` |
| `Relationship type` | Multi-select | `Friend`, `Family`, `Colleague`, `Former colleague`, `Client`, `Prospect`, `Investor`, `Founder`, `Mentor`, `Mentee`, `Advisor`, `Peer`, `Acquaintance`, `Creator`, `Researcher` |
| `Current role` | Text | Job title as of today — useful even when Current company isn't linked |
| `Email` | Email | |
| `Phone` | Phone | |
| `LinkedIn` | URL | |
| `X / Twitter` | URL | |
| `GitHub` | URL | |
| `Website` | URL | |
| `How we met` | Text | Full sentence, future-you context |
| `First met` | Date | Use `date:First met:start`, `date:First met:end` (null usually), `date:First met:is_datetime` = 0 |
| `Birthday` | Date | Same expanded format |
| `Next follow-up` | Date | Same expanded format |
| `Source` | Select | `LinkedIn`, `Twitter/X`, `Conference`, `Warm intro`, `Cold email`, `Newsletter`, `Podcast`, `Friend`, `Work`, `Online community`, `Event`, `Other` |
| `Thoughtfulness notes` | Text | Gifts, personal details, what they value |
| `What they are working on` | Text | Refresh quarterly |
| `What I can offer them` | Text | Reciprocity prompt |
| `Current company` | Relation → Companies | JSON array of company page URLs |
| `Location` | Relation → Places | JSON array |
| `Topics` | Relation → Topics | JSON array |
| `Introduced by` | Relation → People (self) | JSON array, usually 1 person |
| `Mutual connections` | Relation → People (self) | JSON array |
| `Can introduce me to` | Relation → People (self) | JSON array |
| `Should meet` | Relation → People (self) | JSON array |

### Read-only properties (never set these)

| Property | Type | What it does |
|---|---|---|
| `Added on` | Created time | System timestamp |
| `Last edited` | Last edited time | System timestamp |
| `Last interaction` | Rollup | Latest date from linked Interactions |
| `Interaction count` | Rollup | Count of linked Interactions |
| `Days since last contact` | Formula | `dateBetween(now(), Last interaction, "days")`, or 0 if none |
| `Follow-up urgency` | Formula | Tier-based: `🚫 Blocked`, `✨ To meet`, `⏳ Never logged`, `🔴 Overdue`, `🟡 Aging`, `🟢 Fresh` |
| `Interactions` | Back-relation | Auto-populated from Interactions.People |
| `Mentioned in` | Back-relation | Auto-populated from Interactions.Mentioned |

---

## Companies database

Referenced as `<COMPANIES_DS_ID>` and `<COMPANIES_DB_URL>` in examples.

### Writable properties

| Property | Type | Options / notes |
|---|---|---|
| `Name` | Title | Company name |
| `Website` | URL | |
| `LinkedIn` | URL | |
| `X / Twitter` | URL | |
| `Industry` | Multi-select | `AI/ML`, `SaaS`, `Fintech`, `Biotech`, `Consumer`, `Dev tools`, `Climate`, `Hardware`, `Media`, `Healthcare`, `Education`, `Gaming`, `Crypto` |
| `Size` | Select | `Solo`, `2-10`, `11-50`, `51-200`, `201-1000`, `1000+` |
| `Stage` | Select | `Pre-seed`, `Seed`, `Series A`, `Series B`, `Series C+`, `Public`, `Bootstrapped`, `Acquired`, `Shut down` |
| `Founded` | Date | Expanded format |
| `My relationship` | Select | `Customer`, `Vendor`, `Partner`, `Interested in`, `Former employer`, `Current employer`, `Investor target`, `No relationship` |
| `HQ Location` | Relation → Places | |
| `Notes` | Text | |
| `Competitors` | Relation → Companies (self) | |
| `Investors` | Relation → Companies (self) | |
| `Parent company` | Relation → Companies (self) | |
| `Portfolio / subsidiaries` | Relation → Companies (self) | |

### Read-only (auto-populated back-relations)

| Property | What it does |
|---|---|
| `Current people` | Back-ref from People.Current company |
| `Mentioned in interactions` | Back-ref from Interactions.Companies mentioned |

---

## Interactions database

Referenced as `<INTERACTIONS_DS_ID>` and `<INTERACTIONS_DB_URL>` in examples.

### Writable properties

| Property | Type | Options / notes |
|---|---|---|
| `Title` | Title | Scannable, e.g. "Coffee with Alice — April 21" |
| `Date` | Date | Use `date:Date:start`, `date:Date:is_datetime` = 1 for specific times, 0 for day-only |
| `Type` | Select | `In-person meetup`, `Coffee`, `Meal`, `Call`, `Video call`, `Email`, `DM / chat`, `Text / SMS`, `Event / conference`, `Party`, `Walk`, `Other` |
| `Energy` | Select | `Energizing`, `Neutral`, `Draining` |
| `Follow-up needed` | Checkbox | `__YES__` or `__NO__` |
| `Source` | Select | `Calendar-initiated`, `Spontaneous`, `They reached out`, `I reached out` |
| `Summary` | Text | 2-3 sentences |
| `Action items` | Text | Keep concise |
| `People` | Relation → People | Everyone present. Drives the Last interaction rollup! |
| `Mentioned` | Relation → People | People talked about but NOT present. Key for graph edges. |
| `Companies mentioned` | Relation → Companies | |
| `Topics discussed` | Relation → Topics | |
| `Location` | Relation → Places | |

Note: no read-only fields on Interactions — everything is writable.

---

## Topics database

Referenced as `<TOPICS_DS_ID>` and `<TOPICS_DB_URL>` in examples.

### Writable properties

| Property | Type | Options / notes |
|---|---|---|
| `Name` | Title | e.g. "AI safety", "Climate tech", "Bayesian stats" |
| `Category` | Select | `Professional`, `Personal`, `Cultural`, `Scientific`, `Technical`, `Business`, `Creative` |
| `Why I care` | Text | 1-2 sentences, user's perspective |
| `Related topics` | Relation → Topics (self) | Adjacent or overlapping topics |

### Read-only back-relations

| Property | What it does |
|---|---|
| `People interested` | Back-ref from People.Topics |
| `Discussed in` | Back-ref from Interactions.Topics discussed |

---

## Places database

Referenced as `<PLACES_DS_ID>` and `<PLACES_DB_URL>` in examples.

### Writable properties

| Property | Type | Options / notes |
|---|---|---|
| `Name` | Title | e.g. "Mission District", "Ritual Coffee", "San Francisco" |
| `Type` | Select | `City`, `Neighborhood`, `Venue`, `Office`, `Region`, `Country` |
| `Parent place` | Relation → Places (self) | Hierarchical, e.g. Mission District → San Francisco → California → US |
| `Notes` | Text | |

### Read-only back-relations

| Property | What it does |
|---|---|
| `People here` | Back-ref from People.Location |
| `Companies HQ here` | Back-ref from Companies.HQ Location |
| `Interactions here` | Back-ref from Interactions.Location |

---

## Date property expanded format — the universal pattern

Notion dates require three keys per date property, not one. Replace `<n>` with the actual property name.

```json
{
  "date:<n>:start": "2026-04-21",
  "date:<n>:end": null,
  "date:<n>:is_datetime": 0
}
```

- `start`: ISO 8601 date (`YYYY-MM-DD`) or datetime (`YYYY-MM-DDTHH:MM:SSZ`)
- `end`: usually `null`. Only set for date ranges.
- `is_datetime`: `0` for day-only (Birthday, First met, Founded), `1` for specific times (usually Interactions.Date when the user says "at 3pm")

## Relation property format

Relations take a stringified JSON array of page URLs. Even one relation is an array of one.

```json
{
  "Current company": "[\"https://www.notion.so/<company-page-id>\"]"
}
```

Multiple relations:
```json
{
  "Topics": "[\"https://www.notion.so/<topic1>\",\"https://www.notion.so/<topic2>\"]"
}
```

## Common inference shortcuts

When the user is vague, these are safe defaults:

- No `Tier` given → leave empty (surfaces in 📥 Inbox)
- No `Source` given for someone met → `Other`
- No `Status` given for someone met → `Met once`
- No `Status` given for someone online → `Never met - on radar`
- No `Type` on a logged interaction → infer from context ("coffee" → `Coffee`, "call" → `Video call`, "text" → `Text / SMS`, "met up" → `In-person meetup`)
- No `Energy` on a logged interaction → leave empty (don't guess)
- No explicit time → `is_datetime: 0` with today's date

## Schema variations to watch for

The canonical schema above matches the reference design. If the user's CRM diverges, these are the common customizations to check for when a field doesn't behave as expected:

- **Select options added or removed.** Users often add a custom `Relationship type` (e.g., `Therapist`, `Teacher`) or `Source` (e.g., `Hackathon`). If an operation fails because an option isn't found, fetch the People data source schema to see the current list.
- **Formula threshold tweaks.** The `Follow-up urgency` formula thresholds (14/30/90/180 days) may be edited. If the user's "overdue" answers differ from your calculation, fetch the formula property to read the actual values.
- **Renamed fields.** `X / Twitter` might be renamed to `Twitter` or `X`. When an update fails with "property not found," fetch the DB schema and adapt.
- **Two-way self-relations.** The user may have enabled Notion's two-way sync on self-relations, creating paired fields like `Introduced by` ↔ `Introduced me to`. Setting one side auto-populates the other.

When in doubt, `Notion:notion-fetch` the data source (using the `collection://<DS_ID>` URL) to read the current schema. Don't rely on this document if behavior diverges.
