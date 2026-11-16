---
name: x-profile
description: >-
  Score an X (Twitter) profile out of 100 against a 12-part rubric and rewrite
  the parts that lose points: display name, 160-character bio, header,
  pinned post, link. Use when the user says "fix my X profile", "rewrite my
  bio", "score my Twitter", "what should I pin", "optimize my X", or pastes
  their profile and asks how it reads.
license: MIT
---

# x-profile

On X, people find you through a reply or a repost, tap your name, and decide
in about three seconds. They see the name, the photo, the first line of the
bio, the header, and the pinned post. That's the whole pitch.

## Input

Ask the user to paste their display name, handle, bio, location, link and
pinned post, and to say whether they have a header and photo. A screenshot
of the profile works too. If they ask, and the agent has a browser where
they're signed in, it may read their own profile, read only. Read
`~/.x-skills/voice.md` for who they are and the proof they can use.

## Score it

Read `references/rubric.json`: 12 items, 100 points, with what full marks and
zero look like for each. Score every item, show the table, give the total.
Be honest. Most new accounts land in the 20s-40s, and a generous score
doesn't help anyone.

```
X PROFILE  41/100

  pinned post          0/16  nothing pinned
  bio: what you do     6/14  "Developer | Learner" says nothing about what you build
  photo                8/8
  header               0/7   default grey
  ...
```

## Rewrite, biggest loss first

The user has to paste each of these in, so don't hand them everything at once.

**1. Bio (160 characters).** The formula:
`{what you build or do} + {one proof} + {one human detail}`.
Write it in the first person or as a fragment, not "He is". No "passionate",
no "aspiring", no list of six roles, no hashtag wall. Give **three options**,
each checked with `../x-human/scripts/xcheck.py --limit 160 --tags 0-1`, with
the count.

**2. Pinned post.** Either pin the best-performing post (check x-audit or the
log), or write a short intro thread with x-thread: who I am, what I'm
building, what I post here, plus the link. Re-pin when something better comes
along.

**3. Header (1500x500).** One line of positioning and the handle or link, in
the centre (the edges get cropped on mobile). Or a real screenshot of the
project. If the user wants one made, build it as a 1500x500 HTML page and
screenshot it. Use the project's real UI or the user's own brand, never an
invented logo.

**4. Display name (50).** Name, plus an optional short descriptor people
would search ("Sam | building in public").

**5. Link.** The one place a new follower should go next. If they have
several, pick the one that matches the bio.

**6. Photo, location.** Only if they lost points.

## Output

The score table, then the rewrites as copy-ready blocks in fix-first order,
each with its character count. Re-score at the end and show the change
honestly. If the rewrite gets to 74, say 74, and say what the rest needs
(usually a pinned post that performed, a header, and a few weeks of posts,
which a rewrite can't create).

**Changing the live profile is the user's call.** Edit it for them only if
they say yes to the exact text for each field. Never change the handle
without spelling out what breaks (old links and mentions).
