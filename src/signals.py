from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

try:
    import feedparser
except Exception:
    feedparser = None

SOURCES_PATH = Path("data/seeds/signal_sources.csv")
OUTPUT_PATH = Path("data/processed/signals.csv")


def load_sources(path=SOURCES_PATH):
    return pd.read_csv(path)


def simple_impact_score(title, summary=""):
    text = f"{title} {summary}".lower()
    positive_terms = ["funding", "raises", "launch", "partnership", "growth", "revenue", "customers", "acquisition"]
    negative_terms = ["layoff", "shutdown", "fraud", "lawsuit", "down round", "bankrupt", "breach"]
    score = 0
    for term in positive_terms:
        if term in text:
            score += 1
    for term in negative_terms:
        if term in text:
            score -= 2
    return max(-5, min(5, score))


def parse_rss_source(name, category, url, priority):
    if feedparser is None:
        return []
    parsed = feedparser.parse(url)
    rows = []
    for entry in parsed.entries[:20]:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", url)
        published = entry.get("published", "")
        rows.append({
            "source_name": name,
            "source_category": category,
            "source_priority": priority,
            "signal_date": published,
            "title": title,
            "summary": summary,
            "source_url": link,
            "impact_score": simple_impact_score(title, summary),
            "collected_at": datetime.now(timezone.utc).isoformat(),
        })
    return rows


def collect_signals(sources_path=SOURCES_PATH, output_path=OUTPUT_PATH):
    sources = load_sources(sources_path)
    rows = []
    for _, source in sources.iterrows():
        url = str(source.get("url", ""))
        if not url:
            continue
        if "rss" in url or "feed" in url or url.endswith(".xml"):
            rows.extend(parse_rss_source(source["name"], source["category"], url, source["priority"]))
        else:
            rows.append({
                "source_name": source["name"],
                "source_category": source["category"],
                "source_priority": source["priority"],
                "signal_date": "",
                "title": f"Manual review required: {source['name']}",
                "summary": source.get("notes", ""),
                "source_url": url,
                "impact_score": 0,
                "collected_at": datetime.now(timezone.utc).isoformat(),
            })
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    print(collect_signals())
