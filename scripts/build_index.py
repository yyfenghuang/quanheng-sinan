#!/usr/bin/env python3
"""Generate _site/index.html: a plain list of entries, newest first.

One job: render the entry index. Each card links to the entry, shows its date
and description, and renders a repo link when meta.json has repo_url.
"""
from __future__ import annotations

import html

from entries import SITE, load_published

SITE_TITLE = "权衡司南"
SITE_TAGLINE = "以思考的速度。"

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?'
    "family=Noto+Sans:wght@400;600;700&family=Noto+Sans+SC:wght@400;700&"
    "family=Noto+Serif:wght@600;700&family=Noto+Serif+SC:wght@600;700&"
    'display=swap" rel="stylesheet">'
)


def render_card(m):
    slug = m["_slug"]
    title = html.escape(m.get("title", slug))
    date = html.escape(m.get("date", ""))
    desc = html.escape(m.get("description", ""))
    repo = m.get("repo_url")
    repo_link = ""
    if repo:
        repo_link = f'<a class="entry-repo" href="{html.escape(repo)}">代码仓库</a>'
    return f"""    <article class="entry-card">
      <a class="entry-link" href="entries/{slug}/index.html">
        <h2 class="entry-title">{title}</h2>
      </a>
      <p class="entry-meta"><time>{date}</time>{repo_link}</p>
      <p class="entry-desc">{desc}</p>
    </article>"""


def render(items):
    cards = "\n".join(render_card(m) for m in items)
    if not cards:
        cards = '    <p class="empty">暂无条目。</p>'
    return f"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_TITLE}</title>
  {FONTS}
  <link rel="stylesheet" href="templates/style.css">
  <link rel="alternate" type="application/rss+xml" title="{SITE_TITLE}" href="feed.xml">
</head>
<body>
  <main class="index">
    <header class="site-header">
      <h1 class="site-title">{SITE_TITLE}</h1>
      <p class="site-tagline">{SITE_TAGLINE}</p>
      <p class="site-sub"><a href="feed.xml">RSS</a></p>
    </header>
{cards}
  </main>
</body>
</html>
"""


def main():
    SITE.mkdir(exist_ok=True)
    items = load_published()
    (SITE / "index.html").write_text(render(items), encoding="utf-8")
    print(f"index.html: {len(items)} entry(ies)")


if __name__ == "__main__":
    main()
