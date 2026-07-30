#!/usr/bin/env python3
"""Refresh neofetch.svg with live GitHub numbers. Run by .github/workflows/stats.yml.

Standard library + requests only, same dependency footprint as the rest of
this profile's scripts.

Env:
  GITHUB_TOKEN  required (the workflow's built-in token is enough --
                 public repos, stars, followers and the last year of
                 contributions don't need a personal access token)
  GH_LOGIN      account to summarise (default: moiz-codez)
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.neofetch_build import build

API = "https://api.github.com/graphql"

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { totalContributions }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes { stargazers { totalCount } }
    }
    repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, PULL_REQUEST]) {
      totalCount
    }
    followers { totalCount }
  }
}
"""


def fetch(login, token):
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=364)
    variables = {"login": login,
                 "from": f"{start.isoformat()}T00:00:00Z",
                 "to": f"{today.isoformat()}T23:59:59Z"}
    body = json.dumps({"query": QUERY, "variables": variables}).encode()
    req = urllib.request.Request(
        API, data=body,
        headers={"Authorization": f"bearer {token}",
                 "Content-Type": "application/json",
                 "User-Agent": f"{login}-profile-neofetch"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GraphQL errors: {payload['errors']}")
    user = (payload.get("data") or {}).get("user")
    if not user:
        raise SystemExit(f"no such user: {login}")
    return user


def summarise(user):
    repos = user["repositories"]
    stars = sum(n["stargazers"]["totalCount"] for n in repos["nodes"])
    commits_1y = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    return dict(
        repos=f"{repos['totalCount']:,}",
        contributed=f"{user['repositoriesContributedTo']['totalCount']:,}",
        stars=f"{stars:,}",
        commits=f"{commits_1y:,}",
        followers=f"{user['followers']['totalCount']:,}",
    )


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    login = os.environ.get("GH_LOGIN", "moiz-codez")
    out_dir = os.environ.get("OUT_DIR", os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

    stats = summarise(fetch(login, token))
    svg = build(stats)
    path = os.path.join(out_dir, "neofetch.svg")

    old = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = f.read()
    if old == svg:
        print("no change")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"updated {path}: {stats}")


if __name__ == "__main__":
    main()
