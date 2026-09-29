#!/usr/bin/env python3
"""
Fetch Substack RSS feed and export all articles into articles/substack.json.
Zero external dependencies (uses standard library only).
"""

import sys
import os
import json
import urllib.request
import xml.etree.ElementTree as ET

def fetch_substack(publication_or_url: str) -> None:
    if publication_or_url.startswith("http://") or publication_or_url.startswith("https://"):
        feed_url = publication_or_url
    else:
        feed_url = f"https://{publication_or_url}.substack.com/feed"

    print(f"Fetching RSS feed from: {feed_url}")
    req = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "Mozilla/5.0 (OperationalStack-CorpusFetcher/1.0)"}
    )

    with urllib.request.urlopen(req) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    namespaces = {"content": "http://purl.org/rss/1.0/modules/content/"}

    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        pub_date = item.findtext("pubDate") or ""
        content = item.findtext("content:encoded", namespaces=namespaces) or item.findtext("description") or ""

        items.append({
            "title": title,
            "link": link,
            "pubDate": pub_date,
            "content": content
        })

    os.makedirs("articles", exist_ok=True)
    output_path = os.path.join("articles", "substack.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Successfully fetched {len(items)} articles -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_substack.py <substack_subdomain_or_feed_url>")
        sys.exit(1)

    fetch_substack(sys.argv[1])
