import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import lang_stats_build as lsb


class FetchTests(unittest.TestCase):
    def test_fetch_repos_hits_repos_url(self):
        seen = []

        def fake_get_json(url):
            seen.append(url)
            return [{"name": "mojo-OS"}, {"name": "lappu-lang"}]

        names = lsb.fetch_repos("moiz-codez", fake_get_json)
        self.assertEqual(names, ["mojo-OS", "lappu-lang"])
        self.assertIn("users/moiz-codez/repos", seen[0])

    def test_fetch_repo_languages_passes_owner_and_repo(self):
        seen = []

        def fake_get_json(url):
            seen.append(url)
            return {"Python": 100}

        out = lsb.fetch_repo_languages("moiz-codez", "glidemate-ogn", fake_get_json)
        self.assertEqual(out, {"Python": 100})
        self.assertIn("repos/moiz-codez/glidemate-ogn/languages", seen[0])


class AggregationTests(unittest.TestCase):
    def test_fetch_all_languages_aggregates_across_repos(self):
        def fake_get_json(url):
            if "users/moiz-codez/repos" in url:
                return [{"name": "a"}, {"name": "b"}]
            if "a/languages" in url:
                return {"Python": 100}
            if "b/languages" in url:
                return {"Python": 50, "Java": 30}
            raise AssertionError(f"unexpected url: {url}")

        self.assertEqual(
            lsb.fetch_all_languages("moiz-codez", fake_get_json),
            {"Python": 150, "Java": 30},
        )

    def test_compute_percentages_top_n_sorted(self):
        data = {"Java": 30, "Python": 150, "C": 20}
        rows = lsb.compute_percentages(data, top=2)
        self.assertEqual([r[0] for r in rows], ["Python", "Java"])
        self.assertAlmostEqual(sum(r[2] for r in rows), 180.0 / 200.0 * 100, places=6)

    def test_compute_percentages_empty(self):
        self.assertEqual(lsb.compute_percentages({}), [])


class RenderTests(unittest.TestCase):
    def test_build_contains_header_and_footer(self):
        svg = lsb.build({"Python": 150, "Java": 30})
        self.assertIn("LANGUAGE STATS", svg)
        self.assertIn("FIG. 02", svg)
        self.assertTrue(svg.strip().endswith("</svg>"))

    def test_build_lists_each_top_language(self):
        svg = lsb.build({"Python": 150, "Java": 30, "C": 20})
        for name in ("Python", "Java", "C"):
            self.assertIn(name, svg)

    def test_build_uses_animated_fill(self):
        svg = lsb.build({"Python": 150})
        self.assertIn("clipPath", svg)
        self.assertIn("animate", svg)


if __name__ == "__main__":
    unittest.main()
