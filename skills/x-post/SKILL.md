---
name: x-post
description: >-
  Write an X (Twitter) post from a raw idea, a news story or a build update:
  three hook options, one draft that fits X's 280-character count, the
  user's hashtag rule, humanized, never posted or scheduled without an
  explicit yes. Use whenever the user wants a tweet or X post, says "post
  this on X", "tweet about X", "turn this into a tweet", "write today's X
  posts", wants hook options for X, or has a news story to post with their
  take.
license: MIT
---

# x-post

Turns one idea into a post that sounds like the person who posts it, and fits.

## Setup: the voice file (shared by every x-* skill)

All x-* skills keep their files in `~/.x-skills/`:

| file | what | written by |
| --- | --- | --- |
| `voice.md` | handle, timezone, voice, positions, proof, mix, slots, hashtag rule | this skill, once |
| `log.md` | what went out: date, slot, type, hook, first line, tags | x-post, x-thread, x-reply |
| `plan.md` | today's or this week's plan | x-plan |
| `audit.md` | what's working, with dates | x-audit |
| `drafts/` | one file per day | x-daily |

If `~/.x-skills/voice.md` doesn't exist, create it from
`assets/voice-template.md`. If the user already has a voice profile from
another tool (for example a LinkedIn voice file), start from that. Then ask,
in one batched question, for what's still missing: handle, timezone, who
they want to reach, the hashtag rule, and three of their own posts. Write
the file and show it to them. Don't invent a voice. A post in the wrong
voice is worse than no post.

## Before you write

1. **Read `~/.x-skills/voice.md`.**
2. **Read the log** (default `~/.x-skills/log.md`). Don't repeat a story,
   angle or hook from the last 14 days.
3. **Read `references/hooks.json`**: 18 formulas made for 280 chars, each
   with a template, an example, what it's for, and how it gets ruined. The
   examples are illustrations, never facts about the user.
4. **Thin idea** ("post about AI"): ask one batched question. What happened,
   what's the number, and what's your take? A post needs one specific true
   thing.
5. **News:** verify the story from a primary source (web search) before
   writing, and keep the link for the receipt. Never write news from memory.
   Training data is stale, and on X a wrong fact gets quote-posted.

## The shape

X isn't LinkedIn made shorter. The first line is usually the whole post.

```
Line 1    the hook. It has to work if nobody reads further.
Line 2-3  the payoff: the detail, the number, the take. Blank line between.
End       a claim, a punchline, or a question only this post could ask.
Tags      on their own line at the end, per voice.md (default 1-3).
```

- **Length:** aim for 140-260 by X's count. Leave 15-20 chars so the user can
  tweak a word without breaking the limit.
- **One idea.** Two ideas = x-thread or two posts. Say so.
- **Links** go in a reply under the post, not the body. Say so in the receipt.
- **Emoji:** one at most, and only if it does work (the joke, the mood).
- **Media:** if the post is about something visual (UI, terminal, a chart),
  suggest the screenshot to attach. Never fake one.
- **Polls:** for a choice question, write it as a native X poll (2-4 options,
  25 chars each), not as text lines.

## Post types

Match the mix in voice.md. If there's no mix there:

| type | job | non-negotiable |
| --- | --- | --- |
| **NEWS + TAKE** | a real story, with what it means to the reader | the take is the post, verified source |
| **BUILD** | build in public from the user's real work | facts from the repo, git log or the user only |
| **TIP** | one thing the reader can do today | the actual command or steps, and they work |
| **QUESTION** | start replies | specific, answerable in one line |
| **TAKE** | an opinion that could cost a follower | the user actually holds it (voice.md positions) |
| **FLEX** | joke, observation, milestone | still true |

For BUILD posts in a code project, read the repo (`git log --oneline -20`, the
README, the files that changed) and pull one concrete thing. Never claim
users, stars, downloads or performance numbers you didn't read or measure.

## The loop

1. **Three hooks**, from different formulas in `references/hooks.json`, as
   numbered lines. Say which you'd ship and why, in one sentence.
2. **Draft the full post** on the best one.
3. **Check it with the x-human skill:** write the draft to a file, run
   `../x-human/scripts/xcheck.py` with the voice.md hashtag range, and fix
   until READY. Every post from this skill ships checked.
4. **Print the block**, copy-ready, in a fenced block exactly as it should be
   posted. Then the receipt:

```
POST READY
type:      BUILD
hook:      #4 Bug Story
length:    214/280 (X count)
hashtags:  #BuildInPublic #GameDev
check:     1 fix applied, 0 flags  READY
link:      repo link goes in a reply under the post
slot:      12:00 (from your plan)
source:    (news only) the URL you verified it from

Reply "yes" to approve, or tell me what to change.
```

5. **The gate.** Nothing is posted or scheduled without an explicit yes for
   this post or this day's batch. On yes:
   - Append it to the log: date, slot, type, hook #, first line, tags.
   - By default, the user posts it. Only if voice.md says the agent may
     queue approved posts in X's own scheduler, and the agent has a browser
     where the user is already signed in, do that now. Work at a human pace,
     record "scheduled" with the time, and check it shows in the scheduled
     list. Never type the user's password.
   - Never use a third-party auto-poster or an API the user didn't set up and
     ask for.

## Rules that make the difference

- **Never fabricate.** No invented stats, quotes, users, revenue, or "I tried
  X" the user didn't do. If a number is unknown, put `{{number}}` in the draft
  and flag it.
- **No scandal or allegation stories, and no investment advice**, even when
  they're trending. Rumours are written as "reportedly", with the source.
- **No reflex bait.** "Thoughts?", "Agree?", "RT if" are dead and look like
  farming.
- **Don't @ big accounts for reach.** Tag only when they're the subject.
- **A news recap without a take is not a post.** Fifty accounts already
  posted the headline. The take is the only thing that's the user's.

## Example

```
x-post: my free server kept falling asleep so I added a GitHub Action that pings it
```

```
HOOKS
1. #4  Bug Story      My app kept dropping users every 15 minutes. It wasn't a bug. The free server was falling asleep.
2. #18 Ask for Help   My free-tier server sleeps after 15 min idle. I'm pinging it from a GitHub Action. Better free option?
3. #5  Command Drop   Keep a free server awake with a 6-line GitHub Action:

Shipping #1: the reveal is the joke, and every dev who's used a free tier has felt it.
```
