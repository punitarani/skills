# Personal CRM — Query cookbook

Every recipe for answering "find me X" questions against the CRM. When the user asks a question, first check if a pre-built view already answers it — views are the fastest path. Fall back to `notion-search` + filter when no view matches.

## The 16 pre-built views (canonical build)

### People database (8 views)

| View | What it shows | When user asks… |
|---|---|---|
| `📥 Inbox` | People with empty Tier | "what needs processing", "new contacts", "who haven't I triaged" |
| `🔴 Follow up this week` | Follow-up urgency contains "Overdue" | "who should I reach out to", "who's overdue", "follow-up list" |
| `⭐ Inner circle` | Tier = Inner 5 or Close 15, gallery | "my closest people", "inner circle", "best friends list" |
| `✨ On radar (never met)` | Status = Never met - on radar, gallery | "interesting people", "radar list", "who am I tracking online" |
| `💤 Revive` | Status = Dormant or Lost touch | "who have I lost touch with", "dormant relationships", "revive list" |
| `🎂 Birthdays` | Calendar on Birthday field | "whose birthday is coming up", "birthday calendar" |
| `📍 By city` | Board grouped by Location | "who's in [city]", "who's in town", pre-travel queries |
| `🎯 By tier` | Board grouped by Tier | "show me my network by tier", "tier breakdown" |

### Interactions database (4 views)

| View | What it shows | When user asks… |
|---|---|---|
| `📅 Recent` | Table sorted Date DESC | "recent interactions", "what have I been up to" |
| `🗓️ Calendar` | Calendar on Date | "this month's interactions", monthly review |
| `✅ Follow-up needed` | Checkbox = true | "what action items do I have", "pending follow-ups" |
| `🎭 By type` | Board grouped by Type | "coffee meetups", "recent calls", "events I attended" |

### Companies database (2 views)

| View | What it shows | When user asks… |
|---|---|---|
| `🏢 By industry` | Gallery grouped by Industry | "companies in [industry]", industry breakdown |
| `📈 By stage` | Board grouped by Stage | "early-stage companies", "who's at Series A" |

### Topics database (1 view)

| View | What it shows | When user asks… |
|---|---|---|
| `🧭 By category` | Gallery grouped by Category | "what topics am I tracking", "what do people in my network care about" |

### Places database (1 view)

| View | What it shows | When user asks… |
|---|---|---|
| `🗺️ By type` | Board grouped by Type | "what cities have I tracked", "venue list" |

If the user's CRM was built identically to the reference design, all 16 views exist. If some are missing, the query recipes below still work via direct search and filter.

---

## The search tool: scoping by data source

To search within a single database, pass `data_source_url: "collection://<DS_ID>"`:

```
Notion:notion-search(
  query: "Alice",
  query_type: "internal",
  data_source_url: "collection://<PEOPLE_DS_ID>",
  page_size: 5
)
```

Substitute the relevant discovered DS ID (People, Companies, Interactions, Topics, or Places) depending on the question. Always prefer scoped search over workspace-wide search — it's faster and the results are relevant.

---

## Recipe: "Who do I know at [Company]?"

Two strategies, pick whichever is faster:

**A. Back-relation path (best when the company is already in the DB).**

1. Search Companies for the name.
2. `notion-fetch` the company page.
3. Read the `Current people` back-relation — it lists everyone whose `Current company` points here.

**B. Direct search on People.**

1. Search People with the company name as query. This works if the name appears in `How we met` or `Current role`, but misses people where only the relation is set.

Prefer A whenever possible.

---

## Recipe: "Who's in [City] this month?" (pre-travel query)

1. Search Places for the city name to get its page URL.
2. `notion-fetch` the Place page — `People here` back-relation gives you the full list.
3. Filter or sort the user's way by Tier if needed (show Inner 5 first).

If the Place doesn't exist, nobody is tagged to it — suggest the user seed Places.

---

## Recipe: "Who's interested in [topic]?"

1. Search Topics for the topic name.
2. `notion-fetch` the topic page — `People interested` back-relation lists them all.
3. Same page has `Discussed in` back-relation showing every interaction where it came up.

This is the single best demo of why Topics is its own database, not a multi-select.

---

## Recipe: "Who should I follow up with this week?"

The `🔴 Follow up this week` view already has this. Direct the user there, OR fetch the People DB and filter client-side:

```
Notion:notion-search(
  query: "",
  query_type: "internal",
  data_source_url: "collection://<PEOPLE_DS_ID>",
  page_size: 25
)
```

Then for each result, inspect `Follow-up urgency` — the overdue entries contain "Overdue" in the formula result text. Present them sorted by Tier ascending (Inner 5 first).

---

## Recipe: "When did I last talk to [person]?"

1. Search People by name.
2. `notion-fetch` their page.
3. Read `Last interaction` (date) and `Days since last contact` (number). Report both.

If you want the actual conversation, follow the `Interactions` back-relation to see all logged touchpoints, sorted by date.

---

## Recipe: "Who has mutual connections with [person]?"

Graph traversal across People self-relations.

1. Search People for the target name, fetch their page.
2. Read the `Mutual connections` relation — each entry is a person they're connected to.
3. For each connection, fetch and list. Show their Tier, Current company, Location for context.

For deeper graph queries ("who is 2 hops from Alice"), walk the graph manually — this is Notion, not Neo4j; don't try to be clever.

---

## Recipe: "Who has been mentioned a lot but I haven't met?"

This is the "hidden gems" query — people who keep coming up in conversations without being there.

1. Fetch Interactions with filter on `Mentioned` is not empty.
2. Count occurrences of each person in the `Mentioned` field across all interactions.
3. Cross-reference with People to filter Status = `Never met - on radar` or empty.
4. Present top mentioned.

This is a hand-rolled analysis — no pre-built view covers it. Expensive for a big CRM, so warn the user it may take a few tool calls.

---

## Recipe: "Show me active relationships I've been neglecting"

Different from overdue — this targets the gap between "should be active" and "is active".

1. Fetch People with filter: `Status = "Active" AND Days since last contact > 90`.
2. Sort by Days since last contact descending.

These are people the user thinks they're close with but the log says otherwise. High-value for the monthly review.

---

## Recipe: "Recent interactions, last week / last month"

Use the `🗓️ Calendar` view or search Interactions with a date filter:

- Last 7 days: `Date` on or after 7 days ago
- Last 30 days: `Date` on or after 30 days ago
- Last month: `Date` within specified month

Sort by Date descending. If user wants patterns ("how many coffees vs calls"), use the `🎭 By type` view.

---

## Recipe: "On-radar people I found on [source]"

For "Twitter/X people I'm tracking":

1. Search People with filter: `Status = "Never met - on radar" AND Source = "Twitter/X"`.
2. Present with `How we met` (tells you why they're interesting) and `Topics`.

Swap `Source` value for Podcast, Newsletter, LinkedIn, etc.

---

## Recipe: "What do I know about [person]?" — the full briefing

1. Search People by name.
2. `notion-fetch` the page — returns properties AND body content.
3. Summarize in this order:
   - Identity: Name, Current role + Current company, Location
   - Relationship: Tier, Status, How we met, First met, Days since last contact, Follow-up urgency
   - Context: What they are working on, Topics, Thoughtfulness notes
   - Network: Introduced by, Mutual connections
   - Recent: latest 1-3 Interactions (follow the back-relation, fetch and show Summary)

Great prep before a meeting. Takes 2-4 tool calls.

**Deep briefing variant.** If the user is prepping for a meeting ("brief me on X, coffee tomorrow"), offer to augment the CRM data with a light external lookup — recent posts on their X / LinkedIn, news mentions of their company, career changes since you last updated their record. One or two searches, only the last month or so of signal, surfacing things worth mentioning in conversation. Full pattern in `references/enrichment.md` under "Pre-meeting briefings." Always separate "from your CRM" from "from the web" in the response so the user can tell what's fresh.

---

## Recipe: "How many people have I met from [source]?"

Search People with filter `Source = "[source]"`. Count the result. Breakdown by Status if useful.

---

## Tips for composing queries

- **Always start with a view when one exists.** Views are optimized for the UI and return results instantly. Only fall back to search/fetch when no view matches.
- **Scope searches by data source.** Workspace-wide search is slow and noisy.
- **Favor back-relations over filter-by-relation.** Fetching a Company's page and reading `Current people` is one call; searching People with a filter "where Current company contains X" needs the company's URL first AND is less reliable.
- **For complex queries, consider graph traversal.** Fetch one anchor entity, follow relations, fetch related entities. Each fetch is cheap.
- **Show the user the view URL when possible.** If they ask "who's in NYC", searching is fine, but also mention "the 📍 By city view on People groups everyone by location — the NYC column is what you want."
