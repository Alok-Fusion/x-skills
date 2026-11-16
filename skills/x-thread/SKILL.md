---
name: x-thread
description: >-
  Write an X (Twitter) thread: the opener that earns the tap, one idea per
  post, every post checked against X's 280-character count, hashtags only on
  the opener, and the link in the last post. Use when the user says
  "thread", "write a thread", "turn this into a thread", "🧵", when a plan
  has a thread slot, or when an idea has steps, a story or a list too long
  for one post.
license: MIT
---

# x-thread

A thread lives or dies on post 1. Most people only see the opener, in their
feed or as a repost, and decide from that alone. Everything after it is for
the people who already said yes.

## Thread or post?

Use a thread when the idea has **sequence**: steps, a build story with
beats, a list of more than 3 items, a teardown, a "how I built X". If it's
one claim, it's a post. Hand it to the x-post skill and say why. Stretching
one claim over 7 posts is the most common way threads fail.

**4-10 posts.** Under 4 should be a post. Over 12, completion falls off. Split
it into two threads a few days apart.

## Before you write

Same setup as x-post: read `~/.x-skills/voice.md` (x-post creates it if
missing), the log, and `../x-post/references/hooks.json`. For a build thread,
read the repo and git history. Every fact in the thread has to come from
there or from the user.

## Structure

```
1        OPENER    hook + what the reader gets. Stands alone. Hashtags here.
                   An image here if there's a real one (screenshot, diagram).
2        THE STAKE the first real point or the cost. Not background.
3..N-1   ONE IDEA PER POST. Each one makes sense alone, because posts get
                   reposted alone.
N        CLOSE     the recap in one line, plus one action: the link, "follow
                   for part 2", or a specific question. One.
```

- **The opener isn't "A thread 🧵".** That's a label, not a hook. Use a
  formula from hooks.json. A small 🧵 or "(thread)" at the end of post 1 is
  fine if the user likes it.
- **Numbering:** pick one style and keep it. Either none, or `1/` on every
  post, or `1/7` with the right total. The checker verifies it.
- **Hashtags:** only on post 1, using voice.md's range. None on the rest.
- **The link:** in the last post or a reply after it, never in post 1.
- **Each post under ~260** by X's count, so edits don't break the limit.
- **Don't open posts with "And", "Also" or "Next"**. Each post starts like
  it's the first one someone sees.

## The loop

1. **Outline first:** one line per post, so the user can cut or reorder
   before you write 2,000 characters. Give three opener options from
   different hook formulas, and recommend one.
2. **Write it** once the outline is approved, or right away if the user
   said "just write it".
3. **Check it:** write all the posts to one file separated by `---` lines
   and run `../x-human/scripts/xcheck.py thread.txt --tags <voice.md range>`.
   Fix until READY.
4. **Print each post** in its own fenced block with its count, so each copies
   cleanly, then the receipt:

```
THREAD READY  ·  7 posts
opener:    #10 Mistake   "I kept user sessions in server memory for a month."
counts:    212 · 248 · 231 · 260 · 199 · 240 · 187   (all under 280)
hashtags:  #BuildInPublic #WebDev  (post 1 only)
image:     post 1, screenshot of the login screen after a redeploy
link:      repo link in post 7
check:     READY

Reply "yes" to approve, or tell me what to change.
```

5. **The gate.** Same as x-post: explicit yes first, then log it. X's own
   scheduler may not take threads. If it won't, tell the user to post it live
   at the slot and give them the posts in order.

## Rules

- **Never fabricate** a step, a number or a result. A thread has more room to
  pad, so it's where invented detail creeps in. Check every claim against
  the source.
- **Cut the weakest post.** A 6-post thread that's all strong beats a 9-post
  thread with 3 fillers. Say which one you cut.
- **The recap post should work as a screenshot.** That's what gets shared.
