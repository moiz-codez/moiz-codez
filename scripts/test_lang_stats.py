import io
import os
import sys
import unittest
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import lang_stats_build as lsb


def _http_error(code):
    err = urllib.error.HTTPError(
        "https://api.github.com/x", code, "err", {}, io.BytesIO(b""))
    err.close()
    return err


class GetJsonTests(unittest.TestCase):
    def test_retries_transient_error_then_succeeds(self):
        calls = []
        sleeps = []

        def fake_urlopen(request, timeout=None):
            calls.append(request)
            if len(calls) == 1:
                raise _http_error(503)
            return io.BytesIO(b'{"ok": true}')

        result = lsb.get_json("https://api.github.com/x",
                              _urlopen=fake_urlopen,
                              _token=None,
                              _sleep=sleeps.append)
        self.assertEqual(result, {"ok": True})
        self.assertEqual(sleeps, [1])

    def test_exhausts_retries_and_raises_last_error(self):
        def fake_urlopen(request, timeout=None):
            raise _http_error(503)

        with self.assertRaises(urllib.error.HTTPError) as ctx:
            lsb.get_json("https://api.github.com/x",
                         _urlopen=fake_urlopen,
                         _token=None,
                         _sleep=lambda _: None)
        self.assertEqual(ctx.exception.code, 503)

    def test_sends_authorization_header_when_token_provided(self):
        seen = []

        def fake_urlopen(request, timeout=None):
            seen.append(request)
            return io.BytesIO(b'{"ok": true}')

        lsb.get_json("https://api.github.com/x",
                     _urlopen=fake_urlopen,
                     _token="test-token",
                     _sleep=lambda _: None)
        self.assertEqual(seen[0].get_header("Authorization"), "Bearer test-token")

    def test_omits_authorization_header_when_no_token(self):
        seen = []

        def fake_urlopen(request, timeout=None):
            seen.append(request)
            return io.BytesIO(b'{"ok": true}')

        lsb.get_json("https://api.github.com/x",
                     _urlopen=fake_urlopen,
                     _token=None,
                     _sleep=lambda _: None)
        self.assertIsNone(seen[0].get_header("Authorization"))

    def test_non_transient_error_raises_without_retry(self):
        calls = []
        sleeps = []

        def fake_urlopen(request, timeout=None):
            calls.append(request)
            raise _http_error(404)

        with self.assertRaises(urllib.error.HTTPError) as ctx:
            lsb.get_json("https://api.github.com/x",
                         _urlopen=fake_urlopen,
                         _token=None,
                         _sleep=sleeps.append)
        self.assertEqual(ctx.exception.code, 404)
        self.assertEqual(len(calls), 1)
        self.assertEqual(sleeps, [])


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

    def test_build_empty_chart_has_header_but_no_bars(self):
        svg = lsb.build({})
        self.assertTrue(svg.strip().endswith("</svg>"))
        self.assertIn("LANGUAGE STATS", svg)
        self.assertNotIn("langBar", svg)


if __name__ == "__main__":
    unittest.main()
