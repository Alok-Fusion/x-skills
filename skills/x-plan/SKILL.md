---
name: x-plan
description: >-
  Plan the day or week on X (Twitter): which posts go in which slot, the
  specific angle and hook for each, verified news stories to take on, and the
  accounts to reply to. Use when the user says "plan my X", "what should I
  tweet today", "plan today's posts", "content calendar for X", "I have
  nothing to post", or at the start of a daily X routine.
license: MIT
---

# x-plan

The control room. x-post, x-thread and x-reply write things; this decides
what gets written. Run it at the start of the day, or once a week for a
weekly plan.

## Input

1. `~/.x-skills/voice.md`: the mix, the slots, the hashtag rule, what's
   off limits. If it's missing, the x-post skill's setup creates it.
2. `~/.x-skills/log.md`: what went out in the last 14 days. Never repeat a
   story, and never plan a day that's already posted.
3. `~/.x-skills/audit.md` if the x-audit skill has written one. The plan
   follows the user's own evidence over these defaults.
4. What actually happened: new commits in the user's repos
   (`git log --since="2 days ago" --oneline`), anything the user mentions,
   and today's news in their niche.

## What to post

Use the mix in voice.md. If it has none, this works for a small account:

| type | per day | job |
| --- | --- | --- |
| NEWS + TAKE | 1 | be early on a real story, with a take |
| BUILD | 1 | the reason anyone follows a builder |
| TIP | 1 | the bookmark |
| QUESTION | 1 | the replies |
| FLEX | 1 | joke, take or thread |

Never put two of the same type back to back. For each slot give:
- the **type** and the **specific angle**, not a topic. "AI" isn't a plan.
  "A 1T-parameter open model is free to download and still impossible to run
  at home" is a post.
- the **hook number** from `../x-post/references/hooks.json`.
- the **source**: the verified URL for news, the commit or file for BUILD.

**News:** search the web for today's stories in the user's niche, and prefer
primary sources (the company's own post, the repo, the paper). Skip
scandal, allegations, layoff gossip, anything that reads as investment
advice, and stories older than ~48 hours unless the take is new.

**BUILD with no new work?** Use a past decision, a bug, or a "what I'd do
differently" from the git history. Never pad with invented progress.

## When to post

Use the slots in voice.md. Without slots, spread 3-5 posts across the waking
hours of the audience's timezone, not the user's if those differ. Put the
strongest post where the audience is most awake.

Say this plainly: **on a small account, the hour matters far less than
the first line and the replies.** If the user is tuning post times before
their hooks work, they're polishing the wrong thing.

## Who to reply to

At 10-1,000 followers, replies on other people's posts grow an account
faster than more posts. The daily list for x-reply:

- **6 niche accounts**, 10x-100x the user's size, posting today in their field
- **3 peers** at the user's level. This group replies back.
- **1 big account**, but only in the first 30 minutes of a post

Do 15-20 minutes of replies **before** the user's own post goes out, not
after.

## Output

```
X PLAN  ·  Mon 2026-11-16  ·  @yourhandle

09:00  NEWS      #2  News + Take   open 1T model you can download and can't run
                     source: the lab's announcement post (verified)
12:00  BUILD     #4  Bug Story     the free server that kept falling asleep
                     source: commit a1b2c3d
15:00  TIP       #5  Command Drop  find what's holding a port
18:00  QUESTION  #9  Poll          how much of your code does AI write now?
21:00  FLEX      #16 Observation   ...

REPLIES  10 targets for x-reply (6 niche, 3 peers, 1 big)
HASHTAGS per voice.md

Say "write them" and I'll draft all five, or "write 12:00" for one.
```

Write the plan to `~/.x-skills/plan.md`. **Nothing is posted or scheduled
from here.** The drafts go through x-post, and the user's yes comes after
that.
