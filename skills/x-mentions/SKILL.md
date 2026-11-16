---
name: x-mentions
description: >-
  Handle the replies and quote posts on the user's own X (Twitter) posts:
  sort them by which ones are worth answering, then draft the answers. Use
  when the user pastes the replies under their post, says "reply to my
  comments", "someone replied to my tweet", "handle my mentions", or is
  dealing with a critic, a question or a lead on X.
license: MIT
---

# x-mentions

The replies under your own post are where the post gets a second life. Each
answer you give is another engagement event. In the ranking code X
open-sourced in 2023, a reply that the author replied to was one of the
heaviest positive signals, far above a like. The current ranking isn't public
and has changed since, so treat that as direction, not a formula. The
practical rule still holds: **answer the good replies within the first
hour.**

## Input

The user pastes the replies (handle + text), or a screenshot. If they ask,
and the agent has a browser where they're signed in, it may read the replies
on the user's own post. Read only. Quote posts count too: a quote is a reply
in public, and often the most important one. Read `~/.x-skills/voice.md` for
the voice.

## Triage first

Sort every reply into one bucket and say the counts:

| bucket | what it is | what it gets |
| --- | --- | --- |
| **QUESTION** | asks how, what or where | the full answer, in the reply |
| **LEAD** | describes the problem the user solves, or is hiring | a real answer, plus one line of open door |
| **SUBSTANCE** | adds data, disagrees, extends | the longest reply in the thread |
| **PEER** | someone worth being seen talking to | a reply that gives them something back |
| **SUPPORT** | "nice", 🔥, "congrats" | a like, and maybe 2-6 words |
| **NOISE** | bots, crypto/"DM me" spam, bad faith | nothing. Block or report bots, never reply |

Write in that order, and stop when the value stops.

## How to reply

- **Answer the actual question in the reply.** Don't move it to DMs. The
  public answer is what the next reader sees.
- **Match their length.** One line gets one line.
- **To a critic:** agree with the true part first, then hold your point. One
  reply, then stop. Never quote-post a critic to dunk on them.
- **To a lead or a recruiter:** answer in public. The open door is one
  sentence ("happy to share the config if useful"), not a pitch or a
  calendar link.
- **No hashtags in replies**, and no links unless they asked for one.
- **Don't reply to every SUPPORT reply** with a paragraph. A like is enough.
- **Never fabricate.** If they ask for a number the user doesn't have, say
  "haven't measured it" in the draft rather than inventing one.

## Output

Grouped by bucket, counts first, every draft checked with
`../x-human/scripts/xcheck.py --tags 0-0` and shown with its count:

```
REPLIES  ·  on "v2 is out: offline mode"  ·  9 replies
1 QUESTION, 0 LEAD, 2 SUBSTANCE, 1 PEER, 4 SUPPORT, 1 NOISE

QUESTION
@handle: "does offline sync handle conflicts?"
> Last write wins for now. Proper merge is next on the list.  [62/280]

SUBSTANCE
...

SUPPORT  (like all 4, reply to the first)
@handle: "finally" -> It took a while.

NOISE  (1)
A "DM me for promo" bot. Don't reply. Block it.
```

Then the gate: **the user posts the replies.** For factual answers (dates,
versions, specs), check them before drafting. A wrong answer under your
own post costs more than no answer.
