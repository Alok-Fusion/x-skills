#!/usr/bin/env python3
"""Regenerate the README images in .github/assets/.

    banner-dark.png / banner-light.png   the header
    flow-dark.png / flow-light.png       the "How it works" diagram
    checker-demo.png                     real xcheck.py output, before and after

The checker image runs skills/x-human/scripts/xcheck.py on two sample drafts, so it always
shows what the current checker actually prints.

Needs Pillow (`pip install pillow`, ideally built with libraqm so code ligatures stay off)
and the Cascadia Code font (SIL OFL 1.1, https://github.com/microsoft/cascadia-code).

    python3 tools/make_readme_art.py
    python3 tools/make_readme_art.py --only flow
    python3 tools/make_readme_art.py --font ~/fonts/CascadiaCode.ttf
"""

import argparse
import os
import subprocess
import sys
import tempfile

try:
    from PIL import Image, ImageDraw, ImageFont, features
except ImportError:
    sys.exit("Pillow is needed: pip install pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SS = 2  # draw at 2x, then downsample
NOLIG = ["-liga", "-calt"]
FONT_CANDIDATES = [
    "C:/Windows/Fonts/CascadiaCode.ttf",
    os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts/CascadiaCode.ttf"),
    os.path.expanduser("~/Library/Fonts/CascadiaCode.ttf"),
    "/Library/Fonts/CascadiaCode.ttf",
    os.path.expanduser("~/.local/share/fonts/CascadiaCode.ttf"),
    "/usr/share/fonts/truetype/cascadia-code/CascadiaCode.ttf",
    "/usr/share/fonts/opentype/cascadia-code/CascadiaCode.otf",
    "/usr/share/fonts/cascadia-code/CascadiaCode.ttf",
]

# Sample drafts for the checker image: a rushed one, and its rewrite.
DRAFT = "Ship it \u2014 then fix it. Let's delve into why. Thoughts?\n\nhttps://github.com/you/your-repo\n\n#AI\n"
FINAL = ("Ship it, then fix it.\n\nA side project nobody can try teaches you nothing. "
         "A rough one with 3 users teaches you what to fix first.\n\n#BuildInPublic #IndieDev\n")

FONT_PATH = None
RAQM = features.check("raqm")


def font(size, weight="Regular"):
    f = ImageFont.truetype(FONT_PATH, size * SS)
    try:
        f.set_variation_by_name(weight)
    except (OSError, ValueError):
        pass  # a static (non-variable) build of the font: keep its own weight
    return f


def text(d, xy, s_, **kw):
    if RAQM:
        kw["features"] = NOLIG
    d.text(xy, s_, **kw)


def tlen(d, s_, **kw):
    if RAQM:
        kw["features"] = NOLIG
    return d.textlength(s_, **kw)


def s(v):          # banner and checker image
    return int(v * SS)


def sr(v):         # flow diagram
    return int(round(v * SS))


# ----------------------------------------------------------------- banner ---

BANNER = {
    "dark": dict(bg1=(13, 17, 23), bg2=(28, 26, 58), dot=(255, 255, 255, 14), title=(255, 255, 255),
                 tag=(201, 209, 217), dim=(139, 148, 158), chip_bg=(255, 255, 255, 12),
                 chip_bd=(255, 255, 255, 46), chip_tx=(230, 237, 243), accent=(34, 197, 94)),
    "light": dict(bg1=(255, 255, 255), bg2=(238, 241, 255), dot=(15, 23, 42, 16), title=(13, 17, 23),
                  tag=(66, 74, 83), dim=(101, 109, 118), chip_bg=(255, 255, 255, 255),
                  chip_bd=(208, 215, 222, 255), chip_tx=(36, 41, 47), accent=(22, 163, 74)),
}


def banner(theme, out):
    t = BANNER[theme]
    W, H = 1600, 500
    img = Image.new("RGBA", (s(W), s(H)))
    px = img.load()
    for y in range(s(H)):                       # diagonal gradient
        for x in range(0, s(W), 4):
            k = (x / s(W)) * 0.65 + (y / s(H)) * 0.35
            c = tuple(int(t["bg1"][i] + (t["bg2"][i] - t["bg1"][i]) * k) for i in range(3)) + (255,)
            for dx in range(4):
                if x + dx < s(W):
                    px[x + dx, y] = c
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    for gy in range(30, H, 28):                 # faint dot grid
        for gx in range(30, W, 28):
            d.ellipse([s(gx - 1.2), s(gy - 1.2), s(gx + 1.2), s(gy + 1.2)], fill=t["dot"])
    img = Image.alpha_composite(img, over)

    icon = Image.open(os.path.join(ROOT, ".claude-plugin", "icon.png")).convert("RGBA")
    img.alpha_composite(icon.resize((s(250), s(250)), Image.LANCZOS), (s(100), s(125)))

    d = ImageDraw.Draw(img)
    x0 = 420
    text(d, (s(x0), s(92)), "x-skills", font=font(112, "Bold"), fill=t["title"])
    text(d, (s(x0 + 4), s(232)), "Agent skills for growing on X", font=font(34, "SemiBold"), fill=t["tag"])
    text(d, (s(x0 + 4), s(276)), "without sounding like a bot.", font=font(34, "SemiBold"), fill=t["tag"])

    chips = ["10 skills", "X's real 280 count", "Nothing posts without your yes"]
    cf = font(23, "SemiBold")
    cx, cy = x0 + 4, 345
    for i, label in enumerate(chips):
        w = tlen(d, label, font=cf) / SS + (14 if i == 2 else 0)
        box = [s(cx), s(cy), s(cx + w + 44), s(cy + 46)]
        chip = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(chip).rounded_rectangle(box, radius=s(23), fill=t["chip_bg"],
                                               outline=t["chip_bd"], width=s(1.5))
        img = Image.alpha_composite(img, chip)
        d = ImageDraw.Draw(img)
        if i == 2:
            d.ellipse([s(cx + 16), s(cy + 18), s(cx + 26), s(cy + 28)], fill=t["accent"])
            text(d, (s(cx + 34), s(cy + 9)), label, font=cf, fill=t["chip_tx"])
        else:
            text(d, (s(cx + 22), s(cy + 9)), label, font=cf, fill=t["chip_tx"])
        cx = box[2] / SS + 14
    text(d, (s(x0 + 4), s(420)), "Claude Code  ·  Codex  ·  Gemini CLI  ·  GitHub Copilot  ·  Cursor",
         font=font(21), fill=t["dim"])
    if cx >= W - 40:
        sys.exit(f"banner chips overflow the image ({cx:.0f}px): shorten a chip label")
    img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(out, f"banner-{theme}.png"), optimize=True)


# ------------------------------------------------------------------- flow ---

FLOW = {
    "dark": dict(bg=(13, 17, 23), node=(22, 27, 34), border=(61, 68, 77), text=(230, 237, 243),
                 sub=(139, 148, 158), arrow=(110, 118, 129), file=(28, 30, 60), file_bd=(99, 102, 241),
                 yes=(34, 197, 94), yes_fill=(18, 38, 28), check=(57, 197, 207), check_fill=(14, 36, 40),
                 label_bg=(13, 17, 23)),
    "light": dict(bg=(255, 255, 255), node=(246, 248, 250), border=(208, 215, 222), text=(31, 35, 40),
                  sub=(101, 109, 118), arrow=(140, 149, 159), file=(238, 240, 255), file_bd=(99, 102, 241),
                  yes=(22, 163, 74), yes_fill=(236, 253, 243), check=(8, 145, 178), check_fill=(236, 254, 255),
                  label_bg=(255, 255, 255)),
}
NH = 84
ROW = {1: 120, 2: 270, 3: 420}
NODES = {  # name: (x, row, width, title, subtitle, style)
    "voice": (40, 1, 210, "voice.md", "your voice", "file"),
    "plan": (300, 1, 190, "x-plan", "the day's slots", None),
    "write": (550, 1, 270, "x-post · x-thread", "drafts", None),
    "reply": (550, 2, 270, "x-reply", "reply drafts", None),
    "check": (880, 1, 200, "x-human", "checks every draft", "check"),
    "yes": (1140, 1, 190, "Your yes?", "nothing skips this", "yes"),
    "post": (1390, 1, 180, "You post", "or X's scheduler", None),
    "log": (1390, 3, 180, "log.md", "what went out", "file"),
    "audit": (300, 3, 190, "x-audit", "what worked", None),
}


def flow(theme, out):
    t = FLOW[theme]
    W, H = 1600, 560
    img = Image.new("RGB", (sr(W), sr(H)), t["bg"])
    d = ImageDraw.Draw(img)

    def box(name):
        x, r, w = NODES[name][:3]
        return x, ROW[r], x + w, ROW[r] + NH

    def mid(name):
        return (box(name)[0] + box(name)[2]) / 2

    def line(pts, dashed=False, color=None, width=2.2):
        color = color or t["arrow"]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if not dashed:
                d.line([sr(x1), sr(y1), sr(x2), sr(y2)], fill=color, width=sr(width))
                continue
            n = int((((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) // 12)
            for i in range(0, n, 2):
                a, b = i / n, min((i + 1) / n, 1)
                d.line([sr(x1 + (x2 - x1) * a), sr(y1 + (y2 - y1) * a),
                        sr(x1 + (x2 - x1) * b), sr(y1 + (y2 - y1) * b)], fill=color, width=sr(width))

    def arrow(pts, dashed=False, color=None):
        color = color or t["arrow"]
        line(pts, dashed, color)
        (x1, y1), (x, y) = pts[-2], pts[-1]
        L, Wd = 13, 7
        if x > x1:
            tri = [(x, y), (x - L, y - Wd), (x - L, y + Wd)]
        elif x < x1:
            tri = [(x, y), (x + L, y - Wd), (x + L, y + Wd)]
        elif y > y1:
            tri = [(x, y), (x - Wd, y - L), (x + Wd, y - L)]
        else:
            tri = [(x, y), (x - Wd, y + L), (x + Wd, y + L)]
        d.polygon([(sr(a), sr(b)) for a, b in tri], fill=color)

    def label(x, y, s_, color=None, anchor="mm"):
        f = font(16, "SemiBold")
        if anchor == "mm":
            w = tlen(d, s_, font=f) / SS
            d.rounded_rectangle([sr(x - w / 2 - 8), sr(y - 13), sr(x + w / 2 + 8), sr(y + 13)],
                                radius=sr(6), fill=t["label_bg"])
        text(d, (sr(x), sr(y)), s_, font=f, fill=color or t["sub"], anchor=anchor)

    cy = {r: ROW[r] + NH / 2 for r in ROW}
    arrow([(box("voice")[2], cy[1]), (box("plan")[0], cy[1])])
    arrow([(box("plan")[2], cy[1]), (box("write")[0], cy[1])])
    arrow([(box("write")[2], cy[1]), (box("check")[0], cy[1])])
    arrow([(box("check")[2], cy[1]), (box("yes")[0], cy[1])])
    arrow([(box("yes")[2], cy[1]), (box("post")[0], cy[1])], color=t["yes"])
    label((box("yes")[2] + box("post")[0]) / 2, cy[1] - 22, "yes", color=t["yes"])
    px = box("plan")[2] - 40
    arrow([(px, box("plan")[3]), (px, cy[2]), (box("reply")[0], cy[2])])
    rx = mid("check")
    arrow([(box("reply")[2], cy[2]), (rx, cy[2]), (rx, box("check")[3])])
    ex1, ex2, ey = mid("yes"), mid("write"), 62
    arrow([(ex1, box("yes")[1]), (ex1, ey), (ex2, ey), (ex2, box("write")[1])], dashed=True)
    label((ex1 + ex2) / 2, ey, "edit")
    arrow([(mid("post"), box("post")[3]), (mid("post"), box("log")[1])])
    arrow([(box("log")[0], cy[3]), (box("audit")[2], cy[3])], dashed=True)
    ax = box("plan")[0] + 50
    arrow([(ax, box("audit")[1]), (ax, box("plan")[3])], dashed=True)
    label(ax - 14, (box("plan")[3] + box("audit")[1]) / 2, "learns from", anchor="rm")

    styles = {"file": ("file", "file_bd", 1.6), "yes": ("yes_fill", "yes", 2.4),
              "check": ("check_fill", "check", 2.0), None: ("node", "border", 1.6)}
    for name, (_, _, _, title, sub, kind) in NODES.items():
        x0, y0, x1, y1 = box(name)
        fill, bd, bw = styles[kind]
        d.rounded_rectangle([sr(x0), sr(y0), sr(x1), sr(y1)], radius=sr(16), fill=t[fill],
                            outline=t[bd], width=sr(bw))
        text(d, (sr((x0 + x1) / 2), sr(y0 + 31)), title, font=font(23, "SemiBold"), fill=t["text"], anchor="mm")
        text(d, (sr((x0 + x1) / 2), sr(y0 + 59)), sub, font=font(16), fill=t["sub"], anchor="mm")

    img.resize((W, H), Image.LANCZOS).save(os.path.join(out, f"flow-{theme}.png"), optimize=True)


# ----------------------------------------------------------- checker demo ---

def run_xcheck(draft):
    script = os.path.join(ROOT, "skills", "x-human", "scripts", "xcheck.py")
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "post.txt")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(draft)
        res = subprocess.run([sys.executable, script, path, "--tags", "2-3"], capture_output=True,
                             env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if res.returncode != 0:
        sys.exit("xcheck.py failed:\n" + res.stderr.decode("utf-8", "replace"))
    return res.stdout.decode("utf-8").rstrip().splitlines()   # splitlines drops Windows \r


def demo(out):
    C = dict(bg=(13, 17, 23), bar=(22, 27, 34), text=(230, 237, 243), dim=(139, 148, 158),
             prompt=(63, 185, 80), flag=(210, 153, 34), fix=(57, 197, 207), red=(248, 81, 73),
             green=(63, 185, 80), rule=(48, 54, 61))
    f, fb = font(21), font(21, "Bold")
    lh = 31
    blocks = [("draft.txt", run_xcheck(DRAFT)), ("final.txt", run_xcheck(FINAL))]
    W = 1100
    H = 64 + 28 + (sum(len(b[1]) + 1 for b in blocks) + 1) * lh + 24
    img = Image.new("RGBA", (s(W), s(H)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, s(W) - 1, s(H) - 1], radius=s(14), fill=C["bg"], outline=C["rule"], width=s(1))
    d.rounded_rectangle([0, 0, s(W) - 1, s(48)], radius=s(14), fill=C["bar"])
    d.rectangle([0, s(30), s(W) - 1, s(48)], fill=C["bar"])
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([s(20 + i * 24), s(18), s(32 + i * 24), s(30)], fill=col)
    title = "x-human / xcheck.py"
    text(d, (s(W / 2 - tlen(d, title, font=font(16)) / SS / 2), s(14)), title, font=font(16), fill=C["dim"])

    y, x = 64, 28
    for name, lines in blocks:
        text(d, (s(x), s(y)), "$ ", font=fb, fill=C["prompt"])
        text(d, (s(x + 30), s(y)), f"python3 xcheck.py {name} --tags 2-3", font=f, fill=C["text"])
        y += lh
        for ln in lines:
            col, fnt, st = C["text"], f, ln.strip()
            if st.startswith("flag"):
                col = C["flag"]
            elif st.startswith("fix"):
                col = C["fix"]
            elif st.startswith("-----"):
                col = C["rule"]
            elif st.startswith("X CHECK"):
                col = C["dim"]
            elif st.startswith("VERDICT"):
                text(d, (s(x), s(y)), "VERDICT  ", font=fb, fill=C["text"])
                v = st.split("  ", 1)[1].strip()
                text(d, (s(x + tlen(d, "VERDICT  ", font=fb) / SS), s(y)), v, font=fb,
                     fill=C["green"] if v == "READY" else C["red"])
                y += lh
                continue
            elif st.startswith("1  ["):
                fnt = fb
            text(d, (s(x), s(y)), ln, font=fnt, fill=col)
            y += lh
        y += lh * 0.6
    img.resize((W, H), Image.LANCZOS).save(os.path.join(out, "checker-demo.png"), optimize=True)


def main():
    global FONT_PATH
    ap = argparse.ArgumentParser(description="Regenerate the README images.")
    ap.add_argument("--font", help="path to CascadiaCode.ttf")
    ap.add_argument("--out", default=os.path.join(ROOT, ".github", "assets"))
    ap.add_argument("--only", choices=["banner", "flow", "demo"])
    args = ap.parse_args()

    FONT_PATH = args.font or next((p for p in FONT_CANDIDATES if os.path.isfile(p)), None)
    if not FONT_PATH or not os.path.isfile(FONT_PATH):
        sys.exit("Cascadia Code not found. Install it (https://github.com/microsoft/cascadia-code) "
                 "or pass --font /path/to/CascadiaCode.ttf")
    if not RAQM:
        print("note: Pillow has no libraqm, so code ligatures (-> as an arrow) may appear", file=sys.stderr)
    os.makedirs(args.out, exist_ok=True)

    made = []
    if args.only in (None, "banner"):
        banner("dark", args.out), banner("light", args.out)
        made += ["banner-dark.png", "banner-light.png"]
    if args.only in (None, "flow"):
        flow("dark", args.out), flow("light", args.out)
        made += ["flow-dark.png", "flow-light.png"]
    if args.only in (None, "demo"):
        demo(args.out)
        made.append("checker-demo.png")
    print(f"wrote {', '.join(made)} to {os.path.relpath(args.out, ROOT)}")


if __name__ == "__main__":
    main()
