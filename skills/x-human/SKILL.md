---
name: x-human
description: >-
  Check any X (Twitter) post, thread, reply or bio before it goes out: X's
  real weighted character count (links = 23, emoji = 2), hashtag count, links
  in the body, em dashes, curly quotes, invisible characters, AI slop words
  and engagement bait. Use whenever text is headed for X, when the user says
  "will this fit", "count the characters", "does this sound like AI",
  "humanize this tweet", "remove the em dashes", or before any other x-*
  skill shows a draft to the user.
license: MIT
compatibility: Needs Python 3.8+ to run scripts/xcheck.py (standard library only).
---

# x-human

The last gate before anything goes to X. Every x-* skill runs its drafts
through here, so this is the step that actually runs. Don't eyeball it.

```bash
python3 scripts/xcheck.py post.txt --tags 2-3          # check one post
python3 scripts/xcheck.py thread.txt --tags 2-3        # posts separated by a --- line
python3 scripts/xcheck.py post.txt --fix -o clean.txt  # fix the mechanical tells
python3 scripts/xcheck.py post.txt --json              # for scripts
```

Paths are relative to this skill's folder. Use `python` if `python3` is
missing (common on Windows). Take `--tags` from the hashtag rule in
`~/.x-skills/voice.md`. The default is 1-3. Write the draft to a temp file
first. Don't pipe emoji through a shell `echo`, which can mangle them.

## What it checks

| check | what | why |
| --- | --- | --- |
| **LENGTH** | X's weighted count, not `len()` | X counts every link as 23, every emoji as 2, and CJK as 2. A post that looks like 270 can be 296 |
| **HEADROOM** | under 10 chars left | the user can't edit a word without breaking it |
| **HASHTAGS** | count against the range | none = misses discovery, more than 3 reads as spam |
| **LINK IN BODY** | a link in a single post or a thread opener | outbound links tend to get less reach on X. Put it in a reply under the post |
| **FINGERPRINT** | em/en dashes, curly quotes, `…`, invisible chars | no keyboard makes these, and they're the most mechanical tell |
| **SLOP** | delve, leverage, seamless, game-changer ... | shows a plain alternative after the arrow |
| **BAIT** | "Thoughts?", "Agree?", "RT if", "follow for more" | reflex bait reads as a bot |
| **EMOJI / CAPS** | more than 2 emoji, shouting | |
| **THREAD** | numbering is sequential, the total matches, tags only on post 1 | |

The word list is `assets/slop.json`. Users can add their own words, or
keep a flagged word they really use, in `~/.x-skills/slop.json` (same
format, with an `"allow"` list).

## What `--fix` does, and doesn't

It fixes the mechanical tells only: invisible chars deleted (an emoji's own
joiner is kept, so 👨‍💻 survives), em dash to comma, en dash to hyphen, curly
to straight quotes, `…` to `...`, and non-breaking spaces.

It never changes wording. Slop, bait, length and hashtag flags are your job:
rewrite the line by hand, keeping the meaning, and run it again.

## Rewriting what gets flagged

- **Over the limit:** cut the setup line first, then adjectives, then the
  second example. Don't cut the hashtags if voice.md requires them, and don't
  cut the one number.
- **Slop word:** use the plain word the user would say out loud.
- **Bait:** replace it with a question only this post could ask ("Which
  platform broke your first deploy?"), or end on the claim.
- **Link in body:** move it to a reply and say so in the receipt.
- **Structure the script can't see:** "It's not just X, it's Y", three
  parallel fragments in a row ("It plans. It waits. It ships."), a one-word
  question line ("The result?"), and every sentence the same length. Read the
  draft once for these and break them up.

## Be honest about what this is

These are local checks: X's public counting rules plus a list of common AI
tells. Nothing is uploaded. It can't promise what an AI detector or X's
ranking will do, so don't tell the user a post is "undetectable" or "will go
viral".

## Order

1. Write the draft to a file.
2. `xcheck.py --fix -o clean.txt` if there are fixes, then `xcheck.py clean.txt`.
3. Rewrite the flagged lines and check again. READY is the bar. A
   "headroom" note alone is fine.
4. Show the user the cleaned text and the count, e.g. `[247/280] READY`.
   Never show the verdict without the text.
