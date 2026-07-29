#!/usr/bin/env python3
"""Mechanical audit for essayist drafts.

Usage: python slop_check.py <draft.md> [--emdash-per-1000 N]

Checks the mechanics the Pre-publish audit defines. Two layers:

  HARD GATES (exit code 1 on failure — fix, don't argue):
    em-dash budget, " -- " doubles, curly quotes, emoji, rhythm floors
    (share of sub-8-word sentences, presence of 30+-word sentences).

  JUDGMENT REPORTS (exit code unaffected — the model reads and adjudicates):
    banned-vocabulary hits with context (word-boundary matched, annotated when
    inside quotes or likely proper nouns — those are review-not-rewrite),
    negative-parallelism and signposting constructions, -ing analysis tails,
    spec-leakage terms, staccato runs, bullet/numbered lines, candidate
    unsourced stats (digit-bearing sentences with no inline link or named
    source), and the first 110 words for the hook check.

The script cannot judge concessions, callbacks, frames, entity density, or
fabrication — those stay human/model judgment in the audit.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

BANNED_WORDS = [
    # (regex, note) — word-boundary matched, case-insensitive
    (r"delv(?:e|es|ed|ing)", None),
    (r"tapestry", None),
    (r"testament", None),
    (r"underscor(?:e|es|ed|ing)", None),
    (r"pivotal", None),
    (r"crucial(?:ly)?", None),
    (r"vibrant", None),
    (r"robust(?:ly|ness)?", "term of art in stats/engineering — judge"),
    (r"seamless(?:ly)?", None),
    (r"leverag(?:e|es|ed|ing)", "legit as noun/term of art ('leverage ratio') — judge"),
    (r"foster(?:s|ed|ing)?", "common surname — judge"),
    (r"garner(?:s|ed|ing)?", "common surname — judge"),
    (r"showcas(?:e|es|ed|ing)", None),
    (r"elevat(?:e|es|ed|ing)", "literal/medical senses are fine — judge"),
    (r"empower(?:s|ed|ing|ment)?", None),
    (r"unlock(?:s|ed|ing)?", "figurative use only — judge"),
    (r"game-?changer", None),
    (r"paradigm shift", None),
    (r"landscape", "abstract use only; literal landscapes are fine — judge"),
    (r"ecosystem", "abstract use only; biology is fine — judge"),
    (r"boasts?", None),
    (r"stands as", None),
    (r"serves as", None),
    (r"rapidly evolving", None),
    (r"in today's", None),
    (r"it'?s worth noting", None),
    (r"in conclusion", None),
    (r"i hope this helps", None),
    (r"let'?s dive", None),
    (r"here'?s the thing", None),
    (r"at its core", None),
    (r"the real question", None),
    (r"arguably", None),
]
NEG_PARALLEL = r"(?:not just|isn'?t just|not merely|not only|no longer just|it'?s not about)"
ING_TAILS = (r",\s+(?:highlighting|underscoring|showcasing|emphasizing|reflecting|"
             r"symbolizing|demonstrating|signaling|ensuring|fostering|cementing|"
             r"solidifying)\b[^.\n]{0,80}")
SPEC_LEAK = [r"\bconcession\b", r"\bnarrows? the claim\b", r"\bcallback\b",
             r"\bsteelman\b", r"\benemy belief\b", r"\bcoined frame\b"]
NAMED_SOURCE_HINT = re.compile(
    r"\b(?:according to|per |says|said|reports?|reported|estimates?|found|survey|study|census|data from)\b",
    re.I)


def words_of(s):
    return re.findall(r"[\w'$%&€£-]+", s)


def is_emoji(ch):
    o = ord(ch)
    return (0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or
            o in (0x2B50, 0x2B55) or 0xFE00 <= o <= 0xFE0F)


def quote_spans(text):
    spans = []
    for m in re.finditer(r'"[^"\n]{2,400}"|“[^”\n]{2,400}”', text):
        spans.append((m.start(), m.end()))
    return spans


def in_spans(pos, spans):
    return any(a <= pos < b for a, b in spans)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--emdash-per-1000", type=float, default=2.0)
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON too")
    args = ap.parse_args()

    raw = Path(args.file).read_text(encoding="utf-8")
    raw = re.sub(r"```.*?```", "", raw, flags=re.S)
    links = len(re.findall(r"\]\(http", raw))
    body = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)  # keep anchors, drop URLs
    headers = re.findall(r"^#{1,6} .*$", body, flags=re.M)
    bullets = re.findall(r"^\s*(?:[-*+]|\d+[.)]) .*$", body, flags=re.M)

    prose = "\n".join(l for l in body.splitlines() if not l.strip().startswith("#"))
    wc = len(words_of(prose))
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.strip()) > 1]
    slens = [n for n in (len(words_of(s)) for s in sents) if n > 0]
    n = max(1, len(slens))
    short_pct = 100.0 * sum(1 for x in slens if x < 8) / n
    long30 = sum(1 for x in slens if x > 30)

    em = prose.count("—") + len(re.findall(r"\s–\s", prose))
    em_per_1000 = 1000.0 * em / max(1, wc)
    doubles = len(re.findall(r"\s--\s", prose))
    curly = sum(prose.count(c) for c in "“”‘’")
    emoji = sum(1 for ch in prose if is_emoji(ch))

    spans = quote_spans(body)
    vocab_hits = []
    for pat, note in BANNED_WORDS:
        for m in re.finditer(r"(?<![\w-])(" + pat + r")(?![\w-])", body, flags=re.I):
            word = m.group(1)
            ctx = body[max(0, m.start() - 45):m.end() + 45].replace("\n", " ").strip()
            flags = []
            if in_spans(m.start(), spans):
                flags.append("IN-QUOTE: review, don't rewrite")
            if word[:1].isupper() and not re.search(r"[.!?]\s*$",
                                                    body[max(0, m.start() - 3):m.start()]):
                flags.append("capitalized mid-sentence — proper noun? review")
            if note:
                flags.append(note)
            vocab_hits.append({"pattern": pat, "match": word, "context": ctx,
                               "flags": flags})

    neg = [body[max(0, m.start() - 40):m.end() + 60].replace("\n", " ").strip()
           for m in re.finditer(NEG_PARALLEL, body, flags=re.I)]
    ing = [m.group(0).strip() for m in re.finditer(ING_TAILS, body)]
    leaks = []
    for pat in SPEC_LEAK:
        leaks += [body[max(0, m.start() - 40):m.end() + 40].replace("\n", " ").strip()
                  for m in re.finditer(pat, body, flags=re.I)]

    staccato = []
    run = []
    for s, ln in zip(sents, slens):
        if ln <= 5:
            run.append(s)
        else:
            if len(run) >= 3:
                staccato.append(" | ".join(run))
            run = []
    if len(run) >= 3:
        staccato.append(" | ".join(run))

    raw_prose = "\n".join(l for l in raw.splitlines() if not l.strip().startswith("#"))
    raw_sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", raw_prose)
                 if len(s.strip()) > 1]
    unsourced = []
    for s in raw_sents:
        if re.search(r"\d", s) and "](http" not in s and not NAMED_SOURCE_HINT.search(s):
            if len(words_of(s)) >= 6:
                unsourced.append(s[:180])

    gates = [
        ("em-dash budget", em_per_1000 <= args.emdash_per_1000,
         f"{em} em/en dashes = {em_per_1000:.2f}/1000 words (budget {args.emdash_per_1000})"),
        ("no ' -- ' doubles", doubles == 0, f"{doubles} found"),
        ("no curly quotes", curly == 0, f"{curly} found"),
        ("no emoji", emoji == 0, f"{emoji} found"),
        ("rhythm: >=18% sentences under 8 words", short_pct >= 18.0,
         f"{short_pct:.1f}% (target ~20-25%)"),
        ("rhythm: at least one 30+ word sentence", long30 >= 1, f"{long30} found"),
    ]
    failed = [g for g in gates if not g[1]]

    print(f"== SUMMARY: {Path(args.file).name} ==")
    print(f"words {wc} | sentences {len(slens)} | avg {sum(slens)/n:.1f}w "
          f"| <8w {short_pct:.1f}% | >30w {long30} | links {links} "
          f"| headers {len(headers)} | bullet/numbered lines {len(bullets)}")
    print("\n== HARD GATES ==")
    for name, ok, detail in gates:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    print("\n== JUDGMENT REPORTS (adjudicate; quotes/proper nouns are review-not-rewrite) ==")
    print(f"- banned-vocabulary hits: {len(vocab_hits)}")
    for h in vocab_hits[:25]:
        f = ("  [" + "; ".join(h["flags"]) + "]") if h["flags"] else ""
        print(f"    · '{h['match']}': …{h['context']}…{f}")
    print(f"- negative-parallelism candidates: {len(neg)}")
    for s in neg[:8]:
        print(f"    · …{s}…")
    print(f"- '-ing' analysis tails: {len(ing)}")
    for s in ing[:8]:
        print(f"    · {s}")
    print(f"- spec-leakage terms (skill vocabulary in prose): {len(leaks)}")
    for s in leaks[:8]:
        print(f"    · …{s}…")
    print(f"- staccato runs (3+ consecutive <=5-word sentences): {len(staccato)}")
    for s in staccato[:5]:
        print(f"    · {s}")
    print(f"- bullet/numbered lines (licensed only for frameworks/maps/flows): {len(bullets)}")
    for s in bullets[:6]:
        print(f"    · {s.strip()[:120]}")
    print(f"- candidate unsourced stats (digits, no link, no named source in-sentence): {len(unsourced)}")
    for s in unsourced[:12]:
        print(f"    · {s}")
    fw = words_of(prose)[:110]
    print(f"\n== FIRST 110 WORDS (hook check — quotable claim? proper noun/number?) ==\n  {' '.join(fw)}")

    if args.json:
        print("\n== JSON ==")
        print(json.dumps({
            "words": wc, "avg_sentence": round(sum(slens) / n, 1),
            "pct_under_8": round(short_pct, 1), "over_30": long30,
            "em_dashes": em, "em_per_1000": round(em_per_1000, 2),
            "links": links, "headers": len(headers), "bullets": len(bullets),
            "gates_failed": [g[0] for g in failed],
            "vocab_hits": len(vocab_hits), "neg_parallel": len(neg),
            "ing_tails": len(ing), "spec_leaks": len(leaks),
            "staccato_runs": len(staccato), "unsourced_candidates": len(unsourced),
        }, ensure_ascii=False))

    if failed:
        print(f"\nRESULT: {len(failed)} hard gate(s) FAILED — fix before shipping.")
        sys.exit(1)
    print("\nRESULT: hard gates pass. Adjudicate the judgment reports above.")


if __name__ == "__main__":
    main()
