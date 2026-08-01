# Embedded typeface

[JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) v2.304, subset to
printable ASCII plus a handful of punctuation marks the diagrams use (en/em
dash, middle dot, arrow, star), and inlined into every SVG on this profile as
base64 `@font-face` via `scripts/lib/svgkit.py`.

Why inline it at all:

* **These SVGs are loaded through `<img>`.** A browser refuses to fetch
  subresources — including external font URLs — inside an image document, so
  a normal `@font-face { src: url(...) }` pointing off-repo would simply never
  load. A base64 data URI is the only mechanism, and it keeps the page free of
  third-party requests as a side effect.
* **Metrics.** The portrait's character grid assumes an advance width of
  exactly 0.600 em. JetBrains Mono is 600/1000 units, so the geometry lines
  up — but a viewer whose default monospace is narrower (Consolas is ≈0.55)
  would otherwise see the portrait squeezed.

| file | weight | covers |
|---|---|---|
| `jbmono-regular.woff2` | 400 | printable ASCII + a few symbols |
| `jbmono-semibold.woff2` | 600 | same set, semibold |

Licensed under the SIL Open Font License 1.1 — see `OFL.txt`. Subsetting and
redistribution in this form are permitted; the reserved font name is
unchanged.

To regenerate the subset if a new diagram needs a character outside this set,
run `fonttools subset` against `JetBrainsMonoNL-{Regular,SemiBold}.ttf` with
an updated `--text-file`.
