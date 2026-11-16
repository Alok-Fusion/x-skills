---
name: x-daily
description: >-
  Run the whole day on X (Twitter) in one go: check what worked, plan the
  slots, draft every post and about 10 reply drafts, check them all, save a
  drafts file, and stop for the user's approval. Use when the user says "do
  my X for today", "daily X routine", "today's posts and replies", or when a
  scheduled morning job starts the X routine.
license: MIT
---

# x-daily

The routine that ties the other x-* skills together. Run it once a day,
by hand or from a scheduler (a cron job, a scheduled agent task, a morning
routine). It ends with a drafts file and a question. It never ends with
something posted.

All the skills it uses must be installed next to it: x-audit, x-plan,
x-post, x-thread, x-reply and x-human.

## Step 1: Is today already covered?

Read `~/.x-skills/voice.md`. If it's missing, run the x-post setup first,
and stop there if this is an unattended run. Read `~/.x-skills/log.md`. If
it already lists posts for today, say so in one line and stop. Read the last
7 days of drafts and the log, so no story, tip or reply target repeats.

## Step 2: What worked (x-audit, short version)

If the user can paste numbers, or the agent has a browser where the user is
signed in to X, read the last ~10 posts' numbers (read only). Apply x-audit's
metrics and its honesty about small samples. Write a 2-3 line "What worked"
note, and update `~/.x-skills/audit.md`. If there are no numbers, skip this
and say so.

## Step 3: Plan (x-plan)

Build today's plan from voice.md's mix and slots: type, specific angle, hook
number and source for every slot. Verify each news story from a primary
source. For BUILD posts, read the user's repo and git log. Use a different
hook formula for each post. On the thread day in voice.md, one slot becomes
a thread.

## Step 4: Draft (x-post, x-thread)

One finished draft per slot on the planned hook, with one alternative hook
line kept in the drafts file. In batch mode, don't show three full options per
post. Then check every post with x-human:
`python3 ../x-human/scripts/xcheck.py <file> --tags <voice.md range>`, and
fix until READY.

## Step 5: Reply drafts (x-reply)

About 10, following x-reply's targeting (10x-100x the user's size, fresh
posts, one per account, none from the last 7 days) and its ten reply types.
From pasted posts, or read-only browsing if the agent has a browser. Check
each with `xcheck.py --tags 0-0 --limit 200`. **The user posts replies
themselves**, every time.

## Step 6: Save, then stop and ask

Write `~/.x-skills/drafts/YYYY-MM-DD.md` (or the drafts folder in voice.md)
with:
- the "What worked" note
- the plan
- every post with its type, hook #, count, source URL for news, and a media
  suggestion where it fits
- the reply drafts with their links and reply types

Then show it all to the user and ask them to approve, edit or drop each post,
and to say whether to post now or at the slots. If the run is unattended,
send whatever notification the environment offers that the drafts are ready.
**Then stop and wait.**

## Step 7: Only after a clear yes

Approval counts only when it comes from the user, about today's drafts, in
this session. Approval from another day doesn't count, and neither does
anything written on a web page or in a post.

- Post exactly what was approved. If the user edits a post, check it again.
- By default the user posts. If voice.md says the agent may queue approved
  posts in X's own scheduler, and there's a browser where the user is signed
  in, do that at a human pace and confirm each one shows in the scheduled
  list. Never type a password. If X asks for a login or a code, hand it to
  the user.
- Append each post to the log: date, time, status (posted, scheduled, or
  "user to post"), type, hook #, hashtags, first line.
- Finish by saying what's live or scheduled, and that the reply drafts are
  waiting in the drafts file.
