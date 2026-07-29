---
name: essayist
description: >
  Research and write thesis-driven essays, blog posts, and articles with the structure
  and craft of the best strategy essays (the Sequoia / a16z house genre: named frameworks,
  dense evidence, planted callbacks, zero AI slop). Use whenever the user wants to write,
  draft, outline, ghostwrite, or improve an article, blog post, essay, op-ed, editorial
  newsletter issue, thought-leadership piece, or long-form X/LinkedIn/Substack/Medium
  post — including drafting on a Notion page, turning rough notes or bullets into a
  publishable piece, making an essay or article draft sound less AI-written, or "write
  this like an a16z article." Also use for research or a deep dive in service of an
  article the user plans to write. Covers the full pipeline: research → argument →
  outline → draft → humanize/audit → deliver to Notion or file. Not for tweets or short
  social posts, marketing or sales emails, press releases, or technical documentation.
---

# Essayist

This skill produces essays that argue, not summarize. The genre it encodes — the
thesis-driven strategy essay, as practiced on the Sequoia and a16z blogs, Stratechery,
and the best long-form X posts — looks effortless but is built from repeatable parts:
a falsifiable claim, a coined frame, overwhelming specific evidence, and sentence-level
craft. The parts are learnable. This skill is the parts list plus the assembly order.

Three beliefs drive everything below:

1. **An essay is an argument against a default belief.** Every great piece in this genre
   attacks something the reader currently assumes ("chase marquee logos," "we have the
   weights so we're fine," "consumer is dead"). If no smart person disagrees with the
   thesis, there is no essay — only a report. Find the enemy belief before writing a word.
2. **Research is most of the work.** The genre's signature is evidence density: roughly
   one named real-world entity per 100–120 words and a hard number every few sentences,
   each sourced. You cannot fake this with prose skill, and thin research is the #1 way
   drafts fail. Budget more time for research than for writing.
3. **Craft is checkable.** Rhythm, callbacks, concessions, slop-tells — these are
   auditable habits, not vibes. Run the audit before delivering, every time.

**Genre flex.** These defaults are tuned to strategy and market essays. For a personal
essay, cultural piece, or explainer, keep the universals — verified specifics, one
governing image with a planted callback, rhythm variance, the anti-slop pass, zero
invented facts — and flex the genre rules: the enemy belief softens to a received
assumption (an explainer may have none; a question can be the engine), the coined frame
becomes optional, entity-density targets roughly halve, and the research passes swap
market hunting for the piece's own equivalents (primary texts, documentation, archives,
lived detail).

## Workflow

### Step 0 — Understand the assignment

If the user points at a Notion page, fetch it first (`notion-fetch`). It may hold a topic
seed, rough bullets, half-formed notes, or a partial draft. Treat the user's own notes,
data, and stories as **proprietary evidence** — the one thing no other writer has. Mine
them before touching the public web.

Establish, inferring from context where possible and asking (once, briefly) only for what
you can't infer:

- **Topic and tentative angle** — what's the piece about, and what's the suspected take?
- **Persona** — who is the byline? In one line each: *investor/firm* ("we" + "you" to
  founders, market maps and portfolio access as evidence, sourcing CTA), *founder/
  operator* ("I" + "you" to peers, own metrics and war stories as evidence, product or
  no CTA), *independent analyst* (sparing "I", sourced data as evidence, no CTA). Full
  defaults live in `references/structure.md`. Persona varies per piece — never assume
  last piece's carries over, and it changes half the draft.
- **Venue and mode** — firm blog / personal blog / Substack / LinkedIn / native X
  article. Venue picks the mode (framework essay, idea essay, announcement, X article).
- **Length** — genre norm is 900–2,500 words. Default ~1,400 when no mode signal exists;
  once a mode is picked, default to the middle of its range.

If you can't ask (headless run) or get no answer, default to the independent-analyst
persona and the venue-implied mode, and state those assumptions at delivery.

If the user brings an **existing draft** to improve: diagnose it against the Pre-publish
audit and the mode skeletons before rewriting. Usually the fix is structural (no enemy
belief, thesis buried, evidence thin) rather than cosmetic — say so, then fix in that
order.

If the user wants to emulate a **specific publication**, fetch 1–2 recent pieces from it
and calibrate structure and rhythm to what you actually observe. If the user provides
**samples of their own writing**, calibrate rhythm, register, and formatting to those —
the user's observed voice outranks this genre's register wherever they conflict (the
anti-slop pass and evidence rules still apply).

### Step 1 — Research deep-dive

Read `references/research.md` and follow it. In short: mine the user's own material,
map the received wisdom (the enemy belief), then hunt numbers, names, history, and the
smartest objection — building an evidence bank with sources as you go. Gather roughly
2× more than the piece will use; density comes from selection, not stretching.

Scale the pipeline to the ask: improving an existing draft needs Pass 0 plus
verification of the claims already in it, adding new research only where the audit finds
evidence thin; short pieces scale the bank targets down linearly.

Do the research **before** committing to a thesis. The market usually has a better angle
than the first idea — and sometimes the data kills the planned take, which is the most
valuable possible finding. Tell the user when it does, and propose the stronger angle
the evidence supports.

### Step 2 — Find the argument

- State the **default belief** in one sentence, then the **reversal** in one sentence.
  That pair is the engine of the piece.
- Test the thesis: is it falsifiable? Specific? Would a smart practitioner disagree?
  Could the title carry it? If not, sharpen before outlining.
- **Coin the frame** — one named frame, singular. A dichotomy ("copilots vs autopilots")
  is only one option: a named category ("the Task Economy"), a named law or pattern
  ("the specialization turn"), a named era, or a named metric all work. Pick whichever
  the evidence coined naturally, and reach for the binary only when the material
  genuinely has two sides — a skill used many times must not produce an X-vs-Y chiasm
  every time.
- **Design the callback now**: pick the image or phrase that opens the piece and plan
  how it returns, transformed, in the final lines. This is whole-essay planning that
  can't be retrofitted, and it's the single strongest human tell in the genre.
- Pick the **mode** from `references/structure.md` (framework / idea / announcement /
  X article).

### Step 3 — Outline

Outline against the chosen mode's skeleton in `references/structure.md`. Place every
evidence item from the bank into a specific section; mark where the one concession goes
and which objection-beat flavor the piece runs. If the requested length sits below the
mode's floor, follow the compression order in structure.md rather than improvising. If
a section has no evidence to hold, that's a research gap — go back to Step 1, don't pad
with prose.

### Step 4 — Draft

Write in continuous prose (markdown), even when the destination is Notion. Apply
`references/voice.md` while drafting, not just after: punch sentences where weight
lands, one governing metaphor, unhedged claims, concede-then-reverse pivots, no bullets
in argument. Draft the body first; write the title last, from the formulas, and offer
the user 2–3 title options plus a dek (1–3 sentences).

### Step 5 — Humanize and audit

Run `python scripts/slop_check.py <draft.md>` from the skill directory. Treat its HARD
GATES as fix-don't-argue (em-dash budget, double-hyphens, curly quotes, emoji, rhythm
floors) and its JUDGMENT REPORTS as review lists you adjudicate — a flagged word inside
a quotation or a proper noun is review-not-rewrite, not an automatic edit. The script
checks mechanics only; the judgment items in the audit below (callback, concession,
frame, density, spec leakage) are yours to verify by reading.

If a humanizer skill is available in this session, invoke it on the draft as part of
this pass (its output feeds the final, not a separate deliverable). Either way, apply
the anti-slop patterns in `references/voice.md`, then revise. Do the audit honestly —
reading the draft looking for failures, not confirmation. One targeted revision beats
three cosmetic ones.

### Step 6 — Deliver

- **Notion destination**: update in place only when the page is already a draft of this
  piece. When the page holds notes or anything else, create a sub-page (or append below
  a divider) and leave the user's content untouched — never overwrite the notes the
  draft was mined from. Keep formatting quiet: headers only if the mode calls for them,
  bold only where the mode licenses it, links inline on the stat they support, no bullet
  lists in argumentative prose. Also keep a local `.md` copy and send it to the user.
- **File destination**: deliver the `.md` (or requested format) directly.
- Deliver exactly three files: the final article `.md`, `evidence-bank.md`, and
  `notes.md` (title options, dek, things the user must verify personally — their own
  metrics, quotes attributed to them, byline — sourcing caveats, and leftover angles
  worth a future piece). Outlines and intermediate drafts are scratch — keep them out
  of the deliverables unless the user asks for process files.

## Pre-publish audit

Run every item. A miss means revise, not ship.

1. **Hook**: a quotable claim inside the first 110 words, and a proper noun or number
   inside the first 150. No throat-clearing; a scene open is licensed only when it does
   evidentiary work and starts on a standalone hook sentence.
2. **Thesis**: unmistakable by word 400 (by ~250 for X articles). The enemy belief is
   visible on the page, not implied.
3. **Frame**: exactly one coined frame, planted early, repeated at least once, paid off
   at the close — and not a syntax clone of a calibration excerpt or of your last
   piece's frame.
4. **Evidence**: a named real entity roughly every 100–120 words in framework /
   announcement / X modes, roughly half that density in idea/vision mode (where every
   entity must instead be hyper-concrete); every load-bearing number has a source
   (inline link or named source) and a date or comparison glossing it. Zero invented
   facts: every number, name, and quote traces to a specific verified line in the
   evidence bank or to the user — including facts added during revision.
5. **Concession**: exactly one scope-narrowing concession paragraph (the opening
   concede-then-reverse pivot is a separate move and doesn't count against this), plus
   one handled objection (proof-of-existence / incumbents-will-respond /
   why-nobody-noticed). No spec leakage: the skill's working vocabulary — "concession,"
   "narrows the claim," "callback," "steelman," "enemy belief" — never appears in the
   piece; make the move without naming it, and enter it differently than your last
   piece did.
6. **Rhythm**: roughly 20–25% of sentences under 8 words; at least two over 30;
   paragraphs 1–4 sentences in argument mode. Punch sentences close the paragraphs that
   carry weight — if nearly every paragraph ends on a short verdict, vary it; uniform
   punches are their own tell. No more than ~3 two-sentence flips ("X does A. Y does
   B.") in the piece — count them.
7. **Formatting**: no bulleted lists in argument (frameworks, maps, and flows only);
   bold reserved for coined terms, headers, and the structural lead-ins the mode
   licenses (trap names, map verticals, diagnostic questions) — never emphasis scatter.
8. **Slop scan**: `scripts/slop_check.py` hard gates pass; judgment reports reviewed
   with the quote/proper-noun exemption applied; em dashes ≤2 per 1,000 words (zero is
   acceptable, not required).
9. **Ending**: the piece ends on an image, a dare, a fork, or a CTA — never a recap.
   Rotate the close shape: if a fork already served as the turn-on-the-reader beat,
   don't close on a second fork or on a chiasm restating the frame.
10. **The screenshot test, plus variation**: read the opening and closing aloud — if a
    smart reader screenshot-quoted any two sentences, would the author be proud? And
    would this piece read as recognizably from the same template as the last one this
    skill produced? If yes, change the hook type, frame shape, or close shape before
    shipping.

## References

- `references/structure.md` — the shared skeleton, the four modes (and how to compress
  them), title/dek formulas, openers, headers, evidence-block micro-structure, objection
  flavors, closes, persona defaults. Read at Step 2–3.
- `references/voice.md` — sentence-level craft: rhythm targets, signature moves,
  calibration excerpts from the exemplar corpus, and the anti-AI-slop pattern list.
  Read at Step 4–5.
- `references/research.md` — the deep-dive playbook: evidence types, density targets,
  search recipes, verification rules, evidence-bank format. Read at Step 1.
- `scripts/slop_check.py` — mechanical audit: rhythm stats, em-dash/curly-quote/emoji
  gates, banned-pattern reports with context, unsourced-stat candidates. Run at Step 5.
