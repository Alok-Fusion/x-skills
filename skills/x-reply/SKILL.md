---
name: x-reply
description: >-
  Write replies to other people's X (Twitter) posts that read as a person with
  something to add, not a reply-guy or a bot. Picks which posts are worth
  replying to, then drafts a batch the user posts by hand. Use when the user
  pastes a post and wants a reply, says "reply to this", "what do I say
  here", "engage with this", "write my reply drafts", or wants a daily batch
  of replies to bigger accounts.
license: MIT
---

# x-reply

On a small account, your own posts reach your followers, and that might
be 10 people. A good reply under a bigger account's post reaches theirs. It
puts you in front of people who don't know you yet, and on the right post it
gets more views than anything you post yourself. A generic reply gets
nothing, and if it happens often it gets the account muted.

## Input

- **Pasted posts** (text + handle) or screenshots. That's the default.
- **For a daily batch**, if the user asks and the agent has a browser where
  the user is signed in to X, it may find posts by reading X (search, the
  For You feed, or listed accounts). Read only, at a human pace, and never
  like, follow or repost. Record each post's URL.
- If you can't open a URL, ask for the text. Never guess what a post said.

Read `~/.x-skills/voice.md` first. Replies come from the user's positions,
proof and stack, not from general knowledge.

## Pick the right posts

Where you reply matters more than how well you write it.

- **Size:** accounts roughly 10x-100x the user's size in the same niche. A
  mega account with 3,000 replies buries yours, and a 50-follower account
  sends nobody.
- **Freshness:** the first 30-60 minutes, while there are under ~20 replies.
  Replies are mostly read near the top.
- **Fit:** posts where the user actually knows something.
- **Skip:** scandal, politics, outrage bait, giveaways, "reply with your
  @" farming posts, and anything where a reply would read as self-promo.
- **Spread:** no more than one reply per account per day, and not the same
  three accounts every day. Check the log.

## The ten reply types

Pick by what the post actually is. Never default to #10.

| # | type | when | shape |
| --- | --- | --- | --- |
| 1 | **Add a datum** | a claim you can back with a number | "Same here: our build went from 9 min to 2 when..." |
| 2 | **The missing case** | right, but incomplete | "Holds until {condition}. Then..." |
| 3 | **Respectful disagree** | you think it's wrong | agree with the true part first, then the fork |
| 4 | **The receipt** | you did the thing they described | what happened, in one or two lines |
| 5 | **The command** | they asked how, or described a problem | the actual command or fix, nothing else |
| 6 | **Extend one line** | one sentence is the good one | build on it, don't quote it back |
| 7 | **The real question** | the post skipped the hard part | one specific question |
| 8 | **The correction** | a factual error | right, brief, kind, sure, with a source |
| 9 | **The reframe** | right facts, wrong frame | "Another way to read this:" |
| 10 | **The one-liner** | it needs nothing, and you want presence | under 12 words, funny or true |

## Rules

- **1-2 sentences, usually under 200 characters.** Longer reads as a hijack.
- **Never open with** "Great post", "This 💯", "So true", "Facts", "Love
  this", "Couldn't agree more", or the author's name and a "!". Nobody reads
  past them.
- **No emoji opener, no hashtags, no links** unless the link directly answers
  their question.
- **Never restate the post.** They know what they wrote.
- **Never pitch.** No "I built a tool for this 👀" unless they asked for a tool.
  Then give one line and the name, and put the answer first.
- **Say the specific thing.** If the reply could sit under any post on this
  topic, it's noise.
- **Never fabricate** a receipt. "We saw the same thing" needs the user to
  have seen it. If you don't know, use a question or a reframe instead.

## Output

Two options of different types per post, or one each in batch mode, checked
with `../x-human/scripts/xcheck.py --tags 0-0 --limit 200`, with the count:

```
REPLY DRAFTS  ·  10 posts  ·  2026-11-16

1. @somedev · 4.2k followers · posted 25 min ago · 8 replies
   https://x.com/somedev/status/...
   "Free tiers are fine for side projects until they aren't"
   [4 · Receipt]  [112/280]
   Mine slept after 15 min idle and dropped people mid-session. A scheduled
   ping from CI was the $0 fix.
   why: matches a fix in your repo, exact fit, early in the thread

2. ...
```

Then the gate: **the user posts every reply by hand.** X restricts
automated replies, and auto-replying is the fastest way to get an account
limited. Never post, like, follow or repost on the user's behalf for this
skill.

## Log

Append each batch to `~/.x-skills/log.md` under a `## Replies YYYY-MM-DD`
heading, with the handle and post URL. That's how tomorrow's batch avoids the
same accounts.
