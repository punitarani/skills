# humanizer

Forked from [blader/humanizer](https://github.com/blader/humanizer) at version **2.9.1** (commit `523374d`).

`skills/humanizer/SKILL.md` is a verbatim copy of the upstream `SKILL.md`. Everything else in this
directory is packaging to fit the layout of this marketplace. Upstream ships the skill as its own
single-plugin repo with `SKILL.md` at the root; here it lives under `plugins/humanizer/skills/humanizer/`
so it can be installed alongside the other plugins.

Upstream repo files that are build/CI infrastructure rather than skill runtime were not carried over:
`scripts/validate-package.py`, `AGENTS.md`, `agents/openai.yaml`, and the upstream `.claude-plugin/marketplace.json`.

## What it does

Scans text for 33 numbered patterns that mark writing as AI-generated — inflated significance,
promotional language, `-ing` pseudo-analysis, vague attributions, em dashes, rule of three, AI
vocabulary, negative parallelisms, filler and hedging — and rewrites them out while preserving every
claim in the source. It also lists false positives so clean human prose does not get flattened.

## Install

```text
/plugin marketplace add punitarani/skills
/plugin install humanizer@skills
```

## License

MIT, Copyright (c) 2025 Siqi Chen. See [LICENSE](LICENSE) for the upstream notice, retained here as
the license requires.

The skill's pattern list is derived from
[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
maintained by WikiProject AI Cleanup.
