#!/usr/bin/env python3
"""Generate _site/feed.xml from entry metadata.

One job: read every published meta.json and write a valid RSS 2.0 feed, newest
first. No full content in the feed. Readers get the one-sentence description
and follow the link.
"""
from __future__ import annotations

from datetime import datetime, timezone
from email.utils import format_datetime
from xml.etree import ElementTree as ET

from entries import SITE, load_published

BASE_URL = "https://yyfenghuang.github.io/quanheng-sinan"
FEED_TITLE = "权衡司南"
FEED_DESC = "黄宇峰。第一性原理的思考，以思考的速度。"


def to_rfc822(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return format_datetime(dt)


def build(items):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = FEED_TITLE
    ET.SubElement(channel, "link").text = BASE_URL + "/"
    ET.SubElement(channel, "description").text = FEED_DESC
    ET.SubElement(channel, "language").text = "zh-Hans"
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(
        datetime.now(timezone.utc)
    )

    for m in items:
        slug = m["_slug"]
        link = f"{BASE_URL}/entries/{slug}/"
        desc = m.get("description", "")
        repo = m.get("repo_url")
        if repo:
            desc = f"{desc}\n\n代码仓库: {repo}"

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = m.get("title", slug)
        ET.SubElement(item, "link").text = link
        ET.SubElement(item, "guid", isPermaLink="true").text = link
        ET.SubElement(item, "description").text = desc
        if m.get("date"):
            ET.SubElement(item, "pubDate").text = to_rfc822(m["date"])

    return ET.ElementTree(rss)


def main():
    SITE.mkdir(exist_ok=True)
    items = load_published()
    tree = build(items)
    ET.indent(tree, space="  ")
    out = SITE / "feed.xml"
    tree.write(out, encoding="utf-8", xml_declaration=True)
    print(f"feed.xml: {len(items)} item(s) -> {out}")


if __name__ == "__main__":
    main()
