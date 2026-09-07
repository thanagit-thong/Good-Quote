import os
import re
import json
import sys
import numpy as np
from pathlib import Path
from openai import OpenAI


MODEL = os.getenv("MODEL", "gpt-5-mini")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small"
)
THRESHOLD = float(
    os.getenv("SIMILARITY_THRESHOLD", "0.90")
)

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "content" / "Home.md"

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


def normalize(text):
    text = text.lower()

    text = (
        text
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
    )

    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    return re.sub(r"\s+", " ", text).strip()


def existing_quotes(markdown):
    results = []
    category = None

    for line in markdown.splitlines():

        m = re.match(
            r"^##\s+(Work|Life)\s*$",
            line,
            re.I
        )

        if m:
            category = m.group(1).title()
            continue

        m = re.match(
            r"^\s*>\s*(.+?)\s*$",
            line
        )

        if m and category:
            quote = m.group(1).strip()

            results.append({
                "quote": quote,
                "normalized": normalize(quote)
            })

    return results


def embed(texts):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [
        item.embedding
        for item in response.data
    ]


def cosine(a, b):

    a = np.array(a)
    b = np.array(b)

    return float(
        np.dot(a, b)
        /
        (
            np.linalg.norm(a)
            *
            np.linalg.norm(b)
        )
    )


def find_candidate(existing):

    old_quotes = "\n".join(
        f"- {item['quote']}"
        for item in existing
    )

    prompt = f"""
You are the daily quote researcher for a public
GitHub quote collection.

Find exactly ONE genuine quote.

The quote must be about either:

- Work
- Life

Search the web and verify both the quote and
its attribution using the strongest available source.

Prefer:

- primary sources
- books
- transcripts
- speeches
- official archives
- universities
- museums
- reputable publications

Do NOT invent quotes.

Do NOT use unattributed or anonymous quotes.

Do NOT trust quote-aggregation websites alone.

The collection already contains these quotes:

{old_quotes}

The new quote must NOT be:

1. an exact duplicate
2. a punctuation/case/spacing variation
3. a paraphrase
4. essentially the same idea as an existing quote

If a candidate is too similar, discard it and
search again.

Return ONLY valid JSON in this exact structure:

{{
  "quote": "...",
  "author": "...",
  "category": "Work" or "Life",
  "source_url": "https://...",
  "source_note": "brief verification explanation"
}}
"""

    response = client.responses.create(
        model=MODEL,
        tools=[
            {
                "type": "web_search"
            }
        ],
        input=prompt
    )

    text = response.output_text.strip()

    match = re.search(
        r"\{.*\}",
        text,
        re.S
    )

    if not match:
        raise RuntimeError(
            "Model did not return JSON"
        )

    data = json.loads(match.group(0))

    required = [
        "quote",
        "author",
        "category",
        "source_url",
        "source_note"
    ]

    for key in required:

        if not str(
            data.get(key, "")
        ).strip():

            raise RuntimeError(
                f"Missing field: {key}"
            )

    if data["category"] not in [
        "Work",
        "Life"
    ]:
        raise RuntimeError(
            "Invalid category"
        )

    if data["author"].lower() in [
        "unknown",
        "anonymous"
    ]:
        raise RuntimeError(
            "Unacceptable attribution"
        )

    return data


def is_duplicate(candidate, existing):

    normalized_quote = normalize(
        candidate["quote"]
    )

    # Exact / normalized duplicate
    for item in existing:

        if normalized_quote == item["normalized"]:

            return (
                True,
                1.0,
                "normalized duplicate"
            )

    if not existing:

        return (
            False,
            0.0,
            "new collection"
        )

    # Semantic similarity
    vectors = embed(
        [candidate["quote"]]
        +
        [
            item["quote"]
            for item in existing
        ]
    )

    scores = [
        cosine(vectors[0], vector)
        for vector in vectors[1:]
    ]

    best = max(scores)

    if best >= THRESHOLD:

        return (
            True,
            best,
            f"semantic duplicate ({best:.4f})"
        )

    return (
        False,
        best,
        f"accepted ({best:.4f})"
    )


def append_quote(markdown, item):

    if not markdown.strip():

        markdown = (
            "# Good Quotes\n\n"
            "## Work\n\n"
            "## Life\n"
        )

    if not re.search(
        r"^##\s+Work\s*$",
        markdown,
        re.M
    ):
        markdown += "\n## Work\n"

    if not re.search(
        r"^##\s+Life\s*$",
        markdown,
        re.M
    ):
        markdown += "\n## Life\n"

    from datetime import date

    today = date.today().isoformat()

    block = (
        f"\n### {today}\n\n"
        f"> {item['quote']}\n\n"
        f"— {item['author']}\n\n"
        f"*Category: {item['category']}*  \n"
        f"Source: {item['source_url']}\n\n"
        f"---\n"
    )

    heading = f"## {item['category']}"

    position = markdown.find(heading)

    if position < 0:
        raise RuntimeError(
            "Category heading missing"
        )

    position += len(heading)

    return (
        markdown[:position]
        +
        block
        +
        markdown[position:]
    )


def main():

    if HOME.exists():

        markdown = HOME.read_text(
            encoding="utf-8"
        )

    else:

        markdown = ""

    existing = existing_quotes(
        markdown
    )

    # Try up to 10 candidates
    for attempt in range(1, 11):

        candidate = find_candidate(
            existing
        )

        duplicate, score, reason = (
            is_duplicate(
                candidate,
                existing
            )
        )

        print(
            f"Attempt {attempt}: {reason}",
            file=sys.stderr
        )

        if not duplicate:

            HOME.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            new_markdown = append_quote(
                markdown,
                candidate
            )

            HOME.write_text(
                new_markdown,
                encoding="utf-8"
            )

            print(
                json.dumps(
                    candidate,
                    ensure_ascii=False
                )
            )

            return

    raise RuntimeError(
        "Unable to find a unique verified quote "
        "after 10 attempts"
    )


if __name__ == "__main__":
    main()
