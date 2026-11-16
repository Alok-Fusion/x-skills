---
name: x-audit
description: >-
  Post-mortem on what the user already posted on X (Twitter): which posts
  actually worked, why, and what to stop doing, using views, likes, replies,
  reposts and bookmarks. Use when the user says "what's working on X", "why
  did this tweet flop", "audit my X", "read my X analytics", pastes post
  stats, or wants to know what to double down on.
license: MIT
---

# x-audit

Every rule in every X guide, including the ones in these skills, is a guess.
The user's own posts are the evidence. This skill reads them and says what
they show, including when they show nothing yet.

## Input

Whichever the user has:

- **Numbers under each post:** views, likes, replies, reposts, quotes,
  bookmarks. Visible on every post, and enough for a first pass. Pasted or
  screenshots.
- **Premium analytics export** (CSV), if they have Premium. It adds profile
  visits, link clicks and follows.
- **If the user asks**, and the agent has a browser where they're signed
  in, it may read the user's own profile and posts. Their own posts only,
  read only.

Also read `~/.x-skills/log.md`. It records each post's type, hook number,
slot and hashtags, which is what the pattern search needs.

## What to measure

Raw views mostly track follower count and luck. Compute these instead, and
show the working:

| metric | how | what it tells you |
| --- | --- | --- |
| **Engagement rate** | (likes + replies + reposts + quotes + bookmarks) / views | whether the post earned its views |
| **Reply ratio** | replies / likes | whether it started a conversation or just got a nod |
| **Bookmark ratio** | bookmarks / likes | whether it was useful (tips live here) |
| **Reach multiple** | views / followers | whether it travelled past the existing audience |
| **Follow conversion** | follows / profile visits (Premium) | whether the profile closes the deal |

Rank by engagement rate and reach multiple, not raw views.

## Be honest about sample size

With fewer than ~20 posts or ~100 followers, most differences are noise. A
post with 14 views versus 9 means nothing. Only call a pattern when the gap
is big and repeats. Example: if the user's posts about their own work get
3-8x the views of news recaps, every time, that's a signal worth acting on,
because it's the usual pattern for small accounts too. Say how confident
each finding is, and when there's nothing to find yet, say that instead of
inventing a pattern.

## Find the pattern

Put the top 5 and bottom 5 side by side and look at, in this order:

1. **Type**: NEWS, BUILD, TIP, QUESTION, FLEX, thread
2. **Hook formula** (hook # from the log)
3. **Own work vs recap**: did the post say something only this user could say?
4. **Media**: image, poll, plain text
5. **Link in body or not**
6. **Hashtags**: count and which ones
7. **Slot**, checked last and only if 1-6 show nothing. It's almost never
   the cause.

And, separately, **reply activity**: views on days the user did their reply
round versus days they didn't, if the log records it.

## Output

```
X AUDIT  ·  @yourhandle  ·  {n} posts  ·  {date range}  ·  {followers} followers

TOP BY ENGAGEMENT RATE
  {rate}  BUILD   #4  {first line of the post}     {views} views  {replies} replies
  ...
BOTTOM
  {rate}  NEWS    #2  {first line of the post}     {views} views
  ...

WHAT THE DATA SAYS  (small sample, read accordingly)
1. {finding}, with the numbers behind it. n={n}. {how confident}.
2. ...
3. Slot: {usually nothing}. Don't move times on noise.

STOP:     {the thing the data says isn't working}
DO MORE:  {the thing that is}
```

Write it to `~/.x-skills/audit.md` with the date so x-plan builds the next
plan on it. Never fabricate a metric: if a number is missing, leave the cell
blank and say what it would take to get it.
