#!/usr/bin/env python3
"""Check every skill against the Agent Skills spec (agentskills.io/specification)
and every JSON file in the repo. Standard library only. Exit 1 on any problem."""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    fields, key = {}, None
    for line in m.group(1).splitlines():
        top = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if top:
            key, val = top.group(1), top.group(2).strip()
            fields[key] = "" if val in (">-", ">", "|", "|-") else val.strip("'\"")
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def main():
    problems = []
    skills_dir = os.path.join(ROOT, "skills")
    names = sorted(os.listdir(skills_dir))
    for name in names:
        path = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(path):
            problems.append(f"{name}: no SKILL.md")
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        fm = frontmatter(text)
        if fm is None:
            problems.append(f"{name}: no YAML frontmatter")
            continue
        if fm.get("name") != name:
            problems.append(f"{name}: name '{fm.get('name')}' must match the folder")
        if not NAME_RE.match(fm.get("name", "")) or len(fm.get("name", "")) > 64:
            problems.append(f"{name}: name breaks the spec (a-z, 0-9, single hyphens, <= 64)")
        desc = fm.get("description", "")
        if not 1 <= len(desc) <= 1024:
            problems.append(f"{name}: description is {len(desc)} chars (1-1024)")
        if "compatibility" in fm and len(fm["compatibility"]) > 500:
            problems.append(f"{name}: compatibility over 500 chars")
        lines = text.count("\n")
        if lines > 500:
            problems.append(f"{name}: SKILL.md is {lines} lines (spec recommends < 500)")
        refs = set(re.findall(
            r"(?<![\w/~.-])((?:\.\./)?[a-z][\w-]*/(?:[\w.-]+/)*[\w.-]+\.(?:json|py|md))", text))
        for ref in sorted(refs):
            if "YYYY" in ref:          # a pattern like drafts/YYYY-MM-DD.md, not a file
                continue
            target = os.path.normpath(os.path.join(skills_dir, name, ref))
            if not os.path.exists(target):
                problems.append(f"{name}: references missing file {ref}")
        checked_refs = len(refs)
        print(f"ok  {name:12} desc {len(desc):4} chars, {lines:3} lines, {checked_refs} file refs")

    for dirpath, _, files in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep):
            continue
        for f in files:
            if f.endswith(".json"):
                p = os.path.join(dirpath, f)
                try:
                    with open(p, encoding="utf-8") as fh:
                        json.load(fh)
                except ValueError as e:
                    problems.append(f"{os.path.relpath(p, ROOT)}: invalid JSON ({e})")

    with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
        plugin = json.load(fh)
    with open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8") as fh:
        market = json.load(fh)
    with open(os.path.join(ROOT, "gemini-extension.json"), encoding="utf-8") as fh:
        gemini = json.load(fh)
    entry = market["plugins"][0]
    if entry["name"] != plugin["name"]:
        problems.append("marketplace entry name differs from plugin.json name")
    versions = {plugin["version"], entry.get("version", plugin["version"]), gemini["version"]}
    if len(versions) != 1:
        problems.append(f"versions differ across manifests: {sorted(versions)}")

    if problems:
        print("\n" + "\n".join("FAIL " + p for p in problems))
        return 1
    print(f"\nAll {len(names)} skills and manifests pass (version {plugin['version']}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
