#!/usr/bin/env python3
"""
xcheck.py - check a post or thread against X's limits and the machine tells.

What it checks, per post:
  LENGTH     X's weighted character count (the one the compose box uses):
             most Latin, Cyrillic, Devanagari etc. = 1, CJK and most symbols = 2,
             every emoji (including ZWJ and skin-tone sequences) = 2,
             every link = 23 no matter how long. Limit 280 unless --limit.
  HASHTAGS   count against a range (default 1-3; voice.md may say 2-3).
  LINKS      a link in the body of a single post or a thread opener is flagged.
  FINGERPRINT  em dashes, curly quotes, invisible characters, the ellipsis char.
  SLOP       stock AI vocabulary (../assets/slop.json, plus ~/.x-skills/slop.json
             if the user keeps their own list there).
  BAIT       reflex engagement bait: "Thoughts?", "Agree?", "RT if" ...
  THREAD     numbering ("1/", "1/7") is sequential and the total matches.

--fix rewrites the mechanical things only (invisible chars, em/en dashes,
curly quotes, ellipsis, non-breaking spaces). Wording is never changed: the
slop and bait flags need a person, or the model, to rewrite the line.

Input: a text file, or "-" for stdin. A thread is several posts separated by
a line that is just ---

Usage
  python3 xcheck.py post.txt
  python3 xcheck.py thread.txt --tags 2-3
  python3 xcheck.py post.txt --fix -o clean.txt
  python3 xcheck.py post.txt --json
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SLOP_FILE = os.path.join(HERE, "..", "assets", "slop.json")
USER_SLOP = os.path.join(os.path.expanduser("~"), ".x-skills", "slop.json")

# X's weighted ranges (twitter-text v3): these code points weigh 1, all others 2.
LIGHT = [(0x0000, 0x10FF), (0x2000, 0x200D), (0x2010, 0x201F), (0x2032, 0x2037)]
URL_WEIGHT = 23

TLDS = ("com|org|net|io|dev|ai|app|co|in|xyz|me|gg|sh|tech|so|ly|to|tv|"
        "edu|gov|info|biz|site|online|link|page|cloud|us|uk|de|fr|jp")
URL_RE = re.compile(
    r"(?:https?://|www\.)[^\s]+"
    r"|\b[a-z0-9][a-z0-9-]*(?:\.[a-z0-9-]+)*\.(?:" + TLDS + r")\b(?:/[^\s]*)?",
    re.IGNORECASE)
HASHTAG_RE = re.compile(r"(?<![\w&])#(\w*[^\W\d_]\w*)")
MENTION_RE = re.compile(r"(?<![\w])@(\w{1,15})")
NUMBERING_RE = re.compile(r"^\s*(\d{1,2})\s*/\s*(\d{1,2})?(?=\s|$|[.:)])")

BUILTIN_SLOP = [
    "delve", "leverage", "robust", "seamless", "seamlessly", "crucial",
    "tapestry", "testament to", "moreover", "furthermore", "game-changer",
    "game changer", "unlock the", "unleash", "elevate", "revolutionize",
    "revolutionise", "cutting-edge", "ever-evolving", "landscape", "realm",
    "embark", "harness the", "paradigm", "synergy", "in today's",
    "let that sink in", "buckle up", "deep dive", "dive into",
    "it's important to note", "it is important to note", "excited to share",
    "thrilled to", "here's the kicker", "the best part?", "kicked off",
    "foster", "underscore", "pivotal", "meticulous", "intricate", "bustling",
]
BAIT = [
    r"\bthoughts\s*\?", r"\bagree\s*\?", r"\bwho else\b", r"\blike if\b",
    r"\b(?:rt|retweet|repost) if\b", r"\bfollow for more\b",
    r"\blike and (?:rt|retweet|repost)\b", r"\btag (?:a|someone|a friend)\b",
    r"\bcomment below\b", r"\bdrop (?:a|your) .{0,20}below\b",
    r"\bsmash (?:that|the)\b", r"\bdon'?t forget to follow\b",
]
FINGERPRINT = {
    "—": ("em dash", None),
    "–": ("en dash", None),
    "“": ("curly quote", '"'), "”": ("curly quote", '"'),
    "‘": ("curly apostrophe", "'"), "’": ("curly apostrophe", "'"),
    "…": ("ellipsis character", "..."),
    " ": ("non-breaking space", " "), " ": ("narrow nbsp", " "),
}


# ---------------------------------------------------------------- counting ---

def _light(cp):
    return any(a <= cp <= b for a, b in LIGHT)


def _emoji_base(cp):
    return (0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF
            or 0x2B00 <= cp <= 0x2BFF or 0x2300 <= cp <= 0x23FF
            or cp in (0x00A9, 0x00AE, 0x203C, 0x2049, 0x2122, 0x2139, 0x3030,
                      0x303D, 0x3297, 0x3299) or 0x2190 <= cp <= 0x21FF)


def _modifier(cp):
    return (cp == 0xFE0F or cp == 0x20E3 or 0x1F3FB <= cp <= 0x1F3FF
            or 0xE0020 <= cp <= 0xE007F)


def weigh_plain(text):
    """Weighted length of text with no URLs, plus the emoji count."""
    cps = [ord(c) for c in text]
    total = emoji = i = 0
    n = len(cps)
    while i < n:
        cp = cps[i]
        # keycap: 1 + FE0F + 20E3
        if chr(cp) in "0123456789#*" and i + 1 < n and cps[i + 1] in (0xFE0F, 0x20E3):
            i += 1
            while i < n and _modifier(cps[i]):
                i += 1
            total += 2
            emoji += 1
            continue
        if _emoji_base(cp) and (cp >= 0x1F000 or (i + 1 < n and cps[i + 1] == 0xFE0F)
                                or cp >= 0x2600):
            is_flag = 0x1F1E6 <= cp <= 0x1F1FF
            i += 1
            if is_flag and i < n and 0x1F1E6 <= cps[i] <= 0x1F1FF:
                i += 1
            while i < n:
                if _modifier(cps[i]):
                    i += 1
                elif cps[i] == 0x200D and i + 1 < n:
                    i += 2
                else:
                    break
            total += 2
            emoji += 1
            continue
        total += 1 if _light(cp) else 2
        i += 1
    return total, emoji


def weigh(text):
    text = unicodedata.normalize("NFC", text)
    urls = URL_RE.findall(text)
    stripped = URL_RE.sub("", text)
    plain, emoji = weigh_plain(stripped)
    return plain + URL_WEIGHT * len(urls), emoji, urls


# ------------------------------------------------------------------ checks ---

def load_slop():
    """Word -> plain alternative. Built-in list, the bundled file, the user's file."""
    words = {w: "" for w in BUILTIN_SLOP}
    for path in (SLOP_FILE, USER_SLOP):
        try:
            with open(path, encoding="utf-8") as fh:
                lex = json.load(fh)
        except (OSError, ValueError):
            continue
        for e in lex.get("words", []) + lex.get("phrases", []):
            if isinstance(e, dict) and e.get("find"):
                words[e["find"]] = e.get("use", e.get("replace", "")) or ""
        for w in lex.get("allow", []):          # words the user wants to keep
            words.pop(w, None)
    seen, out = set(), []
    for w, use in words.items():
        k = w.lower()
        if k not in seen:
            seen.add(k)
            out.append((w, use))
    return out


def invisible(text):
    """Format (Cf) characters that are not a ZWJ inside an emoji sequence."""
    found = []
    for i, ch in enumerate(text):
        if unicodedata.category(ch) != "Cf":
            continue
        if ch == "‍" and 0 < i < len(text) - 1 and ord(text[i - 1]) > 0x2000 \
                and ord(text[i + 1]) > 0x2000:
            continue
        if 0xE0020 <= ord(ch) <= 0xE007F and i > 0:   # emoji tag sequences
            continue
        found.append(f"U+{ord(ch):04X}")
    return found


def check_post(text, idx, total, args, slop):
    t = text.strip()
    length, emoji, urls = weigh(t)
    tags = HASHTAG_RE.findall(t)
    mentions = MENTION_RE.findall(t)
    fixes, flags = [], []

    counts = {}
    for ch, (name, _) in FINGERPRINT.items():
        if t.count(ch):
            counts[name] = counts.get(name, 0) + t.count(ch)
    fixes += [f"{name} x{n}" for name, n in counts.items()]
    inv = invisible(t)
    if inv:
        fixes.append(f"invisible chars x{len(inv)} ({', '.join(sorted(set(inv)))})")

    low = t.lower()
    hits = []
    for w, use in slop:
        if re.search(r"\b" + re.escape(w.lower()).replace(r"\ ", r"\s+") + r"\b", low):
            hits.append(f"{w} -> {use}" if use else w)
    if hits:
        flags.append("slop: " + ", ".join(hits[:8]))
    for pat in BAIT:
        m = re.search(pat, low)
        if m:
            flags.append(f'bait: "{t[m.start():m.end()]}"')

    over = length - args.limit
    if over > 0:
        flags.append(f"OVER the limit by {over}")
    elif args.limit - length < 10 and total == 1:
        flags.append(f"only {args.limit - length} chars of headroom")

    is_opener = idx == 0
    lo, hi = args.tag_range
    if total == 1 or is_opener:
        if len(tags) < lo:
            flags.append(f"hashtags {len(tags)}, want {lo}-{hi}")
        elif len(tags) > hi:
            flags.append(f"hashtags {len(tags)}, want {lo}-{hi} (more reads as spam)")
        if urls:
            flags.append("link in the body: put it in a reply under the post")
    elif tags:
        flags.append(f"hashtags on post {idx + 1}: keep them on the opener only")

    if emoji > 2:
        flags.append(f"{emoji} emoji: one is plenty")
    caps = [w for w in re.findall(r"\b[A-Z]{4,}\b", t)
            if w not in {"HTTP", "HTTPS", "JSON", "HTML", "REST", "GPU", "GPUS",
                         "CUDA", "AWS", "README", "TODO", "FIFA", "NASA", "UTF"}]
    if len(caps) > 1:
        flags.append("shouting caps: " + ", ".join(caps[:4]))
    if t.startswith(("\U0001F9F5", "A thread", "Thread:", "THREAD")) and total == 1:
        flags.append('a single post that opens like a thread')

    return {
        "n": idx + 1, "length": length, "limit": args.limit, "emoji": emoji,
        "hashtags": tags, "mentions": mentions, "links": urls,
        "fixes": fixes, "flags": flags, "first_line": t.splitlines()[0] if t else "",
    }


def check_numbering(posts):
    nums = []
    for p in posts:
        m = NUMBERING_RE.match(p.strip())
        nums.append((int(m.group(1)), m.group(2)) if m else None)
    if not any(nums):
        return []
    issues = []
    if not all(nums):
        missing = [str(i + 1) for i, x in enumerate(nums) if not x]
        if not (len(missing) == 1 and missing[0] == "1"):   # unnumbered opener is fine
            issues.append("numbering missing on post " + ", ".join(missing))
    start = 1 if nums[0] else 2
    for i, x in enumerate(nums):
        if x and x[0] != i + 1 and x[0] != i + 2 - start:
            issues.append(f"post {i + 1} is numbered {x[0]}")
        if x and x[1] and int(x[1]) != len(posts):
            issues.append(f"post {i + 1} says /{x[1]} but the thread has {len(posts)}")
    return issues


# --------------------------------------------------------------------- fix ---

def fix(text):
    out = []
    for i, ch in enumerate(text):
        cat = unicodedata.category(ch)
        if cat == "Cf":
            keep = ch == "‍" and 0 < i < len(text) - 1 \
                and ord(text[i - 1]) > 0x2000 and ord(text[i + 1]) > 0x2000
            keep = keep or (0xE0020 <= ord(ch) <= 0xE007F and i > 0)
            if not keep:
                continue
        out.append(ch)
    text = "".join(out)
    text = re.sub(r"\s*—\s*", ", ", text)
    text = re.sub(r"(?<=\d)\s*–\s*(?=\d)", "-", text)
    text = re.sub(r"\s+–\s+", ", ", text)
    text = text.replace("–", "-")
    for ch, (_, to) in FINGERPRINT.items():
        if to is not None:
            text = text.replace(ch, to)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    text = re.sub(r"(?m)^,\s*", "", text)
    return text


# -------------------------------------------------------------------- main ---

def split_posts(text):
    parts = re.split(r"(?m)^\s*---\s*$", text)
    return [p.strip("\n") for p in parts if p.strip()]


def render(results, numbering, out):
    kind = "single post" if len(results) == 1 else f"thread of {len(results)}"
    print(f"X CHECK  ·  {kind}", file=out)
    print("-" * 40, file=out)
    ready = True
    for r in results:
        status = "OK" if r["length"] <= r["limit"] else "OVER"
        tag_str = " ".join("#" + t for t in r["hashtags"]) or "none"
        head = f"{r['n']:>2}  [{r['length']}/{r['limit']}] {status}"
        if len(results) == 1 or r["n"] == 1:
            head += f"   tags: {tag_str}"
        print(head, file=out)
        print(f"    {r['first_line'][:72]}", file=out)
        for f in r["fixes"]:
            print(f"    fix   {f}  (--fix handles it)", file=out)
        for f in r["flags"]:
            print(f"    flag  {f}", file=out)
        if r["fixes"] or any(not f.startswith("only ") for f in r["flags"]):
            ready = False
    for issue in numbering:
        print(f"thread  {issue}", file=out)
        ready = False
    print("-" * 40, file=out)
    print("VERDICT  " + ("READY" if ready else "FIX FIRST"), file=out)
    return ready


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("file", help="text file, or - for stdin")
    ap.add_argument("--limit", type=int, default=280, help="per-post limit (280)")
    ap.add_argument("--tags", default="1-3", help="hashtag range, e.g. 2-3")
    ap.add_argument("--fix", action="store_true", help="print the cleaned text")
    ap.add_argument("-o", "--output", help="write cleaned text here (with --fix)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    lo, _, hi = args.tags.partition("-")
    args.tag_range = (int(lo), int(hi or lo))

    if args.file == "-":
        text = sys.stdin.read()
    else:
        with open(args.file, encoding="utf-8-sig") as fh:
            text = fh.read()

    if args.fix:
        text = fix(text)
        if args.output:
            with open(args.output, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text.strip() + "\n")

    posts = split_posts(text)
    if not posts:
        print("nothing to check", file=sys.stderr)
        return 2
    slop = load_slop()
    results = [check_post(p, i, len(posts), args, slop) for i, p in enumerate(posts)]
    numbering = check_numbering(posts) if len(posts) > 1 else []

    if args.json:
        print(json.dumps({"posts": results, "thread": numbering}, ensure_ascii=False, indent=2))
        return 0
    if args.fix and not args.output:
        print(text.strip())
        print()
    render(results, numbering, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
