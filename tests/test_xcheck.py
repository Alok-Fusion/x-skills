"""Tests for skills/x-human/scripts/xcheck.py. Run: python -m unittest discover tests"""

import argparse
import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = importlib.util.spec_from_file_location(
    "xcheck", os.path.join(ROOT, "skills", "x-human", "scripts", "xcheck.py"))
xcheck = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(xcheck)


def args(limit=280, tags=(1, 3)):
    return argparse.Namespace(limit=limit, tag_range=tags)


def check(text, idx=0, total=1, **kw):
    return xcheck.check_post(text, idx, total, args(**kw), xcheck.load_slop())


class WeightedLength(unittest.TestCase):
    def test_plain_ascii_counts_one_each(self):
        self.assertEqual(xcheck.weigh("hello world")[0], 11)

    def test_every_link_counts_23(self):
        long_url = "https://github.com/someone/" + "a" * 120
        self.assertEqual(xcheck.weigh("see " + long_url)[0], 4 + 23)
        self.assertEqual(xcheck.weigh("x.com")[0], 23)

    def test_filenames_are_not_links(self):
        n, _, urls = xcheck.weigh("Node.js README.md")
        self.assertEqual(urls, [])
        self.assertEqual(n, len("Node.js README.md"))

    def test_emoji_and_sequences_count_two(self):
        for e in ["😅", "👨‍💻", "🇮🇳", "1️⃣", "❤️‍🔥", "👍🏽"]:
            with self.subTest(e=e):
                self.assertEqual(xcheck.weigh(e), (2, 1, []))

    def test_cjk_counts_two_and_devanagari_one(self):
        self.assertEqual(xcheck.weigh("日本")[0], 4)
        self.assertEqual(xcheck.weigh("नमस्ते")[0], len("नमस्ते"))


class Checks(unittest.TestCase):
    def test_clean_post_has_no_flags(self):
        r = check("Write the README before the code.\n\n#DevTips #Programming", tags=(2, 3))
        self.assertEqual(r["flags"], [])
        self.assertEqual(r["fixes"], [])

    def test_over_limit(self):
        r = check("a" * 300 + " #AI")
        self.assertTrue(any("OVER" in f for f in r["flags"]))

    def test_hashtag_range(self):
        self.assertTrue(any("hashtags 0" in f for f in check("no tags here", tags=(2, 3))["flags"]))
        self.assertTrue(any("hashtags 4" in f for f in check("#a1 #b2 #c3 #d4")["flags"]))

    def test_number_is_not_a_hashtag(self):
        self.assertEqual(check("we are #1 #AI")["hashtags"], ["AI"])

    def test_link_in_body_flagged(self):
        r = check("new release https://example.com #AI")
        self.assertTrue(any("link in the body" in f for f in r["flags"]))

    def test_slop_and_bait(self):
        flags = " ".join(check("Let's delve into this. Thoughts? #AI")["flags"])
        self.assertIn("delve", flags)
        self.assertIn("bait", flags)

    def test_fingerprint_reported(self):
        r = check("It works — mostly. “quoted”​ #AI")
        joined = " ".join(r["fixes"])
        self.assertIn("em dash", joined)
        self.assertIn("curly quote x2", joined)
        self.assertIn("invisible", joined)


class Fix(unittest.TestCase):
    def test_fix_cleans_mechanical_tells_only(self):
        out = xcheck.fix("It works — mostly… “ok”​ 5–10 tests")
        self.assertEqual(out, 'It works, mostly... "ok" 5-10 tests')

    def test_fix_keeps_emoji_joiners(self):
        self.assertEqual(xcheck.fix("👨‍💻 ❤️‍🔥"), "👨‍💻 ❤️‍🔥")


class Thread(unittest.TestCase):
    def test_split_on_dashes(self):
        self.assertEqual(len(xcheck.split_posts("one\n---\ntwo\n---\nthree")), 3)

    def test_numbering_gap(self):
        issues = xcheck.check_numbering(["1/ a", "2/ b", "4/ c"])
        self.assertTrue(any("numbered 4" in i for i in issues))

    def test_numbering_total(self):
        issues = xcheck.check_numbering(["1/5 a", "2/5 b", "3/5 c"])
        self.assertTrue(any("/5" in i for i in issues))

    def test_good_numbering(self):
        self.assertEqual(xcheck.check_numbering(["1/3 a", "2/3 b", "3/3 c"]), [])

    def test_hashtags_only_on_opener(self):
        r = check("more detail #AI", idx=1, total=3)
        self.assertTrue(any("opener only" in f for f in r["flags"]))


if __name__ == "__main__":
    unittest.main()
