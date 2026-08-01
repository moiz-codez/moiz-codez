"""Layout + content for neofetch.svg, shared by the one-off builder and the
GitHub Actions refresh script so the two never drift out of sync."""
import math
from datetime import date

from . import svgkit

# Backed out from "21 years, 6 months, 1 day" as of the day this profile was
# built. Nudge this if it's a day or two off from your actual birthday.
BIRTH_DATE = date(2005, 1, 29)

MASCOT_COLS, MASCOT_ROWS = 30, 24
RAMP = " .:-=+*#%@"


def uptime_string(today=None):
    today = today or date.today()
    years = today.year - BIRTH_DATE.year
    months = today.month - BIRTH_DATE.month
    days = today.day - BIRTH_DATE.day
    if days < 0:
        months -= 1
        # days in previous month
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month > 1 else today.year - 1
        from calendar import monthrange
        days += monthrange(prev_year, prev_month)[1]
    if months < 0:
        years -= 1
        months += 12
    plural = lambda n: "" if n == 1 else "s"
    return f"{years} year{plural(years)}, {months} month{plural(months)}, {days} day{plural(days)}"


def mascot_lines():
    """Abstract diamond-ring glyph -- generated geometry, not borrowed art."""
    def shade(cx, cy):
        x, y = cx - MASCOT_COLS / 2, (cy - MASCOT_ROWS / 2) * 1.9
        d = abs(x) + abs(y)
        rings = [(18, 0.15), (15, 0.55), (11, 0.15), (8, 0.75), (4, 0.15), (0, 1.0)]
        best = 0
        for r, v in rings:
            band = abs(d - r)
            if band < 1.6:
                best = max(best, v * (1 - band / 1.6))
        return best

    out = []
    for r in range(MASCOT_ROWS):
        row = "".join(RAMP[min(len(RAMP) - 1, int(shade(c + 0.5, r + 0.5) * len(RAMP)))]
                      for c in range(MASCOT_COLS))
        out.append(row.rstrip())
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


# key -> value rows. `None` values are computed while rendering.
ROWS = [
    ("OS", "Windows 11 \u00b7 Android 16 \u00b7 Ubuntu"),
    ("Uptime", None),  # computed
    ("Kernel", "B.S. Computer Science, MUET \u201927"),
    ("IDE", "VS Code"),
    ("", ""),
    ("Languages", "C \u00b7 C++ \u00b7 Java \u00b7 Python \u00b7 JavaScript \u00b7 Dart"),
    ("Frameworks", "React \u00b7 Next.js \u00b7 Express \u00b7 Flask \u00b7 Django \u00b7 FastAPI"),
    ("Data", "MongoDB \u00b7 PostgreSQL \u00b7 MySQL \u00b7 Redis \u00b7 Firebase \u00b7 Supabase"),
    ("DevOps", "Docker \u00b7 Kubernetes \u00b7 AWS \u00b7 GCP \u00b7 Vercel \u00b7 Netlify \u00b7 GH Actions"),
    ("Tools", "Git \u00b7 Linux \u00b7 Android Studio \u00b7 Postman \u00b7 Nginx"),
    ("", ""),
    ("Hobbies", "Football \u00b7 Hockey \u00b7 Reading"),
    ("", ""),
    ("Email", "moiz.codez@gmail.com"),
    ("LinkedIn", "moiz-siyal"),
    ("Reddit", "u/moiz-codez"),
]
