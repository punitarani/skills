# skills

A Claude Code plugin marketplace shipping a few personal skills.

## Plugins

| Plugin | What it does |
|--------|--------------|
| [`personal-crm`](plugins/personal-crm) | Operate a Notion Personal CRM (People / Companies / Interactions / Topics / Places) — capture contacts, log meetings, query follow-ups. |
| [`market-intelligence`](plugins/market-intelligence) | Build, enrich, verify, and activate competitive intelligence in Obsidian vaults; map relationships and ship outreach lists. |
| [`grill-me`](plugins/grill-me) | Stress-test plans and designs by interviewing one decision at a time. |
| [`humanizer`](plugins/humanizer) | Strip the tells of AI-generated writing out of prose. Forked from [blader/humanizer](https://github.com/blader/humanizer). |

## Install

In Claude Code:

```text
/plugin marketplace add punitarani/skills
/plugin install personal-crm@skills
/plugin install market-intelligence@skills
/plugin install grill-me@skills
/plugin install humanizer@skills
```

Pick whichever plugins you want — they install independently.

## Local development

To work on this marketplace from a local checkout:

```text
/plugin marketplace add /Users/punit/projects/skills
```

After editing a manifest or skill, run `/plugin marketplace update skills` to pick up changes.

## License

MIT — see [LICENSE](LICENSE).

`humanizer` is a fork of third-party work and carries its own MIT notice, Copyright (c) 2025 Siqi Chen — see [plugins/humanizer/LICENSE](plugins/humanizer/LICENSE).
