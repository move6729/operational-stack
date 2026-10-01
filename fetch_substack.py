#!/usr/bin/env python3
"""
Fetch complete Substack publication archive and export all articles into articles/substack.json.
Zero external dependencies (uses standard library only).
"""

import sys
import os
import json
import urllib.request
import xml.etree.ElementTree as ET

def fetch_substack(publication_or_url: str) -> None:
    if publication_or_url.startswith("http://") or publication_or_url.startswith("https://"):
        host = publication_or_url.split("//")[-1].split("/")[0]
        subdomain = host.split(".")[0]
    else:
        subdomain = publication_or_url

    base_api_url = f"https://{subdomain}.substack.com/api/v1/posts"
    print(f"Fetching complete post archive from: {subdomain}.substack.com")

    items = []
    limit = 50
    offset = 0

    while True:
        api_url = f"{base_api_url}?limit={limit}&offset={offset}"
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "Mozilla/5.0 (OperationalStack-CorpusFetcher/1.0)"}
        )

        try:
            with urllib.request.urlopen(req) as response:
                raw_data = response.read().decode("utf-8")
                posts = json.loads(raw_data)
        except Exception:
            break

        if not posts:
            break

        for post in posts:
            title = post.get("title") or ""
            link = post.get("canonical_url") or f"https://{subdomain}.substack.com/p/{post.get('slug', '')}"
            pub_date = post.get("post_date") or ""
            content = post.get("body_html") or post.get("description") or ""

            items.append({
                "title": title,
                "link": link,
                "pubDate": pub_date,
                "content": content
            })

        if len(posts) < limit:
            break

        offset += limit

    if not items:
        feed_url = f"https://{subdomain}.substack.com/feed"
        print(f"API returned 0 posts. Falling back to RSS feed: {feed_url}")
        req = urllib.request.Request(
            feed_url,
            headers={"User-Agent": "Mozilla/5.0 (OperationalStack-CorpusFetcher/1.0)"}
        )
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        namespaces = {"content": "http://purl.org/rss/1.0/modules/content/"}

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
