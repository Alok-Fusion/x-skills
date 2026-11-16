---
name: x-repurpose
description: >-
  Turn one long thing (a LinkedIn post, blog, README, YouTube video,
  podcast, transcript, or a project's git history) into a week of X (Twitter)
  posts plus a thread. Use when the user says "repurpose this for X", "turn my
  LinkedIn post into tweets", "post this on X too", "I have a video or
  blog", or pastes long content and wants it on X.
license: MIT
---

# x-repurpose

One good long piece holds four to six X posts. Most people paste the
LinkedIn post into X, cut it at 280 and lose the best part.

## Input

Any long asset: a LinkedIn post, a blog, a README, a talk transcript, a call
summary, or a repo. For a repo, read the README, `git log`, and the files
that changed most. For a video URL, use a transcript tool if one is
available; otherwise ask the user to paste the text. Read all of it before
pulling anything out.

## Extract, don't summarise

A summary isn't a post. Pull out the things that stand alone:

| pull | what it is | becomes |
| --- | --- | --- |
| **Claims** | sentences that would start an argument | TAKE posts |
| **Numbers** | figures, durations, counts, versions | BUILD or milestone posts |
| **Stories** | a moment with a problem and a cost | Bug Story / Mistake posts |
| **Mechanisms** | "the way it works is..." | TIP posts, or a thread |
| **Commands** | real commands, configs, snippets | Command Drop posts |
| **Lines** | sentences already quotable as they are | one-liners |

List what you found, with counts, before writing anything. If there are
fewer than four items, the source is thin. Say so rather than stretching it.

## LinkedIn → X

The same idea, a different shape:

- **The hook becomes the whole post.** LinkedIn's line 1 plus its turn is
  often a complete X post.
- **Cut the setup.** LinkedIn earns the "see more" slowly. X readers decide
  in a line.
- **900 characters is a thread, not a post.** If the LinkedIn post has steps,
  it's an x-thread.
- **Drop "link in comments", the LinkedIn hashtag footer, and "Agree?"**.
  Use the hashtag rule from voice.md.
- **Don't post both on the same hour with the same words.** Rewrite for X,
  and space them out.

## Build the week

Each extract becomes one post that stands completely alone. The reader
hasn't seen the video and never will, so never write "as I said in my
video". Give each one a different hook formula from
`../x-post/references/hooks.json`. Five posts with the same shape reads as a
content mill. Fit them into the type mix and slots in `~/.x-skills/voice.md`,
and check the log so nothing repeats.

```
SOURCE  LinkedIn post "our deploy checker now explains its fixes" (1,240 chars)
FOUND   2 claims, 4 numbers, 1 story, 2 mechanisms, 1 command, 3 lines

WEEK
Tue  BUILD  #4  Bug Story     the port your platform injects at runtime
Wed  TIP    #5  Command Drop  the one command, and what it catches
Thu  TAKE   #1  Hot Take      "it works on my machine" isn't done
Sat  THREAD #10 Mistake       the deploy that broke silently, step by step

Say "write Tuesday" and I'll draft it.
```

Then draft on request, one at a time, through x-post or x-thread (which run
the x-human check). Don't dump five finished posts at once. They'll sound
the same, and the user won't edit any of them. Every fact stays as it was
in the source. Repurposing never adds a number the source didn't have.
