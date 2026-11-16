# x-skills

**Agent skills for growing on X (Twitter) without sounding like a bot.** Plan
the day, write posts and threads that fit X's real character count, draft
replies to bigger accounts, handle your mentions, see what actually worked,
and fix your profile.

It works with any AI agent that reads [Agent Skills](https://agentskills.io)
(`SKILL.md` folders): Claude Code, OpenAI Codex, Gemini CLI, GitHub Copilot,
Cursor and others. **Nothing is ever posted without your yes.**

<p align="center"><img src=".claude-plugin/icon.png" width="120" alt="x-skills icon"></p>

## What's inside

| skill | what it does |
| --- | --- |
| **x-daily** | runs the whole morning: what worked → plan → drafts → reply drafts → checks → stops for your approval |
| **x-plan** | today's (or this week's) slots: type, specific angle, hook, verified source, plus 10 accounts to reply to |
| **x-post** | three hook options, then one post that fits 280 by X's count, with your hashtag rule |
| **x-thread** | outline first, then a thread: the opener earns the tap, one idea per post, tags only on post 1 |
| **x-reply** | picks posts worth replying to (10-100x your size, under an hour old) and drafts replies in 10 types. You post them |
| **x-mentions** | sorts the replies under your own posts (question, lead, critic, bot...) and drafts answers |
| **x-audit** | engagement rate, reply ratio, bookmark ratio, reach multiple, and honesty about small samples |
| **x-profile** | scores your profile out of 100 on a 12-part rubric and rewrites the bio, pinned post and header |
| **x-repurpose** | turns a LinkedIn post, blog, README, video transcript or git history into a week of X posts |
| **x-human** | the last check on everything: X's weighted count, hashtags, links, em dashes, invisible characters, AI words, bait |

They share one settings file, `~/.x-skills/voice.md`, so every skill writes in
your voice and follows your routine.

## Install

The skills refer to each other (everything runs through x-human's checker,
and x-post holds the hook library), so **install the whole pack**, not single
skills.

### Claude Code

```bash
claude plugin marketplace add Alok-Fusion/x-skills
```

```bash
claude plugin install x-skills@alok-fusion
```

Or inside a session: `/plugin marketplace add Alok-Fusion/x-skills`, then
`/plugin install x-skills@alok-fusion`. The skills show up as
`/x-skills:x-post`, `/x-skills:x-daily` and so on, and Claude also picks them
up on its own when you ask for a tweet.

### Gemini CLI

```bash
gemini extensions install https://github.com/Alok-Fusion/x-skills
```

### Codex, GitHub Copilot, Cursor, and anything else that reads SKILL.md

Clone it and run the installer:

```bash
git clone https://github.com/Alok-Fusion/x-skills.git
```

```bash
cd x-skills && ./install.sh
```

On Windows PowerShell, run `.\install.ps1` instead.

The installer copies the skills into both shared folders, and each tool picks
up the one it reads:

| folder | read by |
| --- | --- |
| `~/.agents/skills/` | Codex, Gemini CLI, GitHub Copilot |
| `~/.claude/skills/` | Claude Code, Cursor, GitHub Copilot |

Use `--target agents` or `--target claude` (`-Target` in PowerShell) for
just one, or `--target <folder>` for any other skills folder. If a tool shows
every skill twice, reinstall with a single target. In Claude Code, use either
the plugin or the installer, not both. Run `./install.sh --uninstall` to remove
them. It leaves your `~/.x-skills/` files alone, and it never replaces an
`x-*` skill it didn't install unless you pass `--force`.

**Needs:** Python 3.8+ for the checker (standard library only). For the
daily routine, a web search tool for news. A browser tool is optional, for
reading your own post numbers.

## First run

Ask your agent for a post, e.g. *"write an X post about the bug I fixed
today"*. The first time, x-post creates `~/.x-skills/voice.md` from
[the template](skills/x-post/assets/voice-template.md) and asks a few
questions: your handle, timezone, who you're writing for, your hashtag rule,
and three of your own posts so it can match your voice. Or fill the file in
yourself first.

Then, every day:

- *"do my X for today"* runs **x-daily**
- *"plan my X week"* runs **x-plan**
- *"reply to these"* plus the pasted posts runs **x-reply**
- *"what's working on my X?"* plus your numbers runs **x-audit**
- *"turn this LinkedIn post into tweets"* runs **x-repurpose**

To run it every morning, point your tool's scheduler (a cron job, a scheduled
agent task, a routine) at *"run the x-daily skill"*. It stops with a drafts
file and waits for you.

## The checker on its own

```bash
python3 skills/x-human/scripts/xcheck.py post.txt --tags 2-3
```

```
X CHECK  ·  single post
----------------------------------------
 1  [84/280] OK   tags: #AI
    Ship it — then fix it. Let's delve into why. Thoughts?
    fix   em dash x1  (--fix handles it)
    flag  slop: delve -> dig into / look at
    flag  bait: "Thoughts?"
    flag  hashtags 1, want 2-3
    flag  link in the body: put it in a reply under the post
----------------------------------------
VERDICT  FIX FIRST
```

(That post also has a GitHub link on its own line, which counts as 23 however
long the URL is.)

It counts the way X's compose box does: a link is 23 no matter how long, an
emoji is 2 (including 👨‍💻 and flag sequences), CJK is 2, and Latin, Cyrillic
and Devanagari are 1. Put threads in one file with a `---` line between
posts. `--fix` cleans only the mechanical tells (dashes, curly quotes,
invisible characters). Wording is always left to you. Add your own words, or
allow ones you really use, in `~/.x-skills/slop.json`.

## What it will never do

- **Post, reply, like, follow or schedule without your explicit yes** for
  those exact posts. Replies are always posted by you, by hand. X restricts
  automated replies.
- **Make things up.** No invented stats, users, quotes, or "I tried X" you
  didn't do. A missing number becomes `{{number}}` and gets flagged.
- **Post news from memory.** Every story is checked against a primary source,
  and the source goes in the receipt.
- **Chase scandal, allegations or investment tips**, even when they're trending.
- **Promise virality.** The checks are local heuristics plus X's public
  counting rules. They can't predict X's ranking or an AI detector.

## Files it keeps

Everything lives in `~/.x-skills/`: `voice.md` (your setup), `log.md` (what
went out, so nothing repeats), `plan.md`, `audit.md`, and `drafts/`. It's
plain Markdown, so you can read and edit all of it.

## Development

```bash
python3 tools/validate.py
```

```bash
python3 -m unittest discover -s tests
```

`validate.py` checks every skill against the
[Agent Skills spec](https://agentskills.io/specification) (names, description
length, file references) and that the Claude, marketplace and Gemini
manifests agree. CI runs both, plus an install/uninstall round trip.

## Credits

Made by [Alok Kushwaha](https://github.com/Alok-Fusion). Inspired by
the LinkedIn skill packs that exist for Claude, after finding nothing like
them for X. MIT licensed, see [LICENSE](LICENSE).
