import os
import re
import json
import subprocess
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

    text = re.sub(
        r"https?://\S+",
        "",
        text
    )

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


def read_wiki_home():
    """
    Clone the existing GitHub Wiki and read Home.md.
    """

    repository = os.environ["REPOSITORY"]

    wiki_url = (
        f"https://x-access-token:"
        f"{os.environ['GITHUB_TOKEN']}"
        f"@github.com/"
        f"{repository}.wiki.git"
    )

    wiki_dir = ROOT / ".wiki"

    if wiki_dir.exists():
        subprocess.run(
            [
                "git",
                "-C",
                str(wiki_dir),
                "pull",
                "--ff-only"
            ],
            check=True
        )

    else:
        subprocess.run(
            [
                "git",
                "clone",
                wiki_url,
                str(wiki_dir)
            ],
            check=True
        )

    wiki_home = wiki_dir / "Home.md"

    if not wiki_home.exists():
        raise RuntimeError(
            "Wiki Home.md was not found"
        )

    return wiki_home.read_text(
        encoding="utf-8"
    )


def existing_quotes(markdown):

    quotes = []

    for line in markdown.splitlines():

        # GitHub Wiki currently uses:
        #
        # ### "quote"
        #
        # or:
        #
        # ### 🌟 "quote"

        match = re.match(
            r"^###\s+(?:🌟\s*)?[\"“](.+?)[\"”]\s*$",
            line.strip()
        )

        if match:
            quote = match.group(1).strip()

            quotes.append({
                "quote": quote,
                "normalized": normalize(quote)
            })

    return quotes


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
You are the daily quote researcher for
the Good Quote GitHub Wiki.

Find exactly ONE genuine quote.

The quote must belong to exactly one
of these categories:

- Work
- Life

You MUST search the web.

You MUST verify:
1. the exact wording
2. the author
3. a reliable source

Prefer primary or highly reputable sources,
including books, speeches, transcripts,
official archives, universities, museums,
and reputable publications.

Do NOT invent quotes.

Do NOT use Anonymous.

Do NOT use Unknown.

Do NOT rely only on quote aggregation websites.

These quotes already exist in the collection:

{old_quotes}

The new quote MUST NOT be:

- an exact duplicate
- a punctuation variation
- a case variation
- a spacing variation
- a paraphrase
- substantially the same idea

If the candidate is similar to an existing quote,
discard it and search again.

Return ONLY JSON:

{{
  "quote": "...",
  "author": "...",
  "category": "Work" or "Life",
  "source_url": "https://...",
  "source_note": "brief explanation of verification"
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
            "Model did not return valid JSON"
        )

    data = json.loads(
        match.group(0)
    )

    required = [
        "quote",
        "author",
        "category",
        "source_url",
        "source_note"
    ]

    for field in required:

        if not str(
            data.get(field, "")
        ).strip():

            raise RuntimeError(
                f"Missing field: {field}"
            )

    if data["category"] not in [
        "Work",
        "Life"
    ]:
        raise RuntimeError(
            "Invalid category"
        )

    if data["author"].lower() in [
        "anonymous",
        "unknown"
    ]:
        raise RuntimeError(
            "Anonymous/Unknown attribution"
        )

    return data


def is_duplicate(candidate, existing):

    normalized = normalize(
        candidate["quote"]
    )

    # --------------------------------
    # Exact / normalized duplicate
    # --------------------------------

    for item in existing:

        if normalized == item["normalized"]:

            return (
                True,
                1.0,
                "normalized duplicate"
            )

    if not existing:

        return (
            False,
            0.0,
            "collection is empty"
        )

    # --------------------------------
    # Semantic duplicate
    # --------------------------------

    texts = [
        candidate["quote"]
    ]

    texts.extend(
        item["quote"]
        for item in existing
    )

    vectors = embed(texts)

    scores = [
        cosine(
            vectors[0],
            vector
        )
        for vector in vectors[1:]
    ]

    best = max(scores)

    if best >= THRESHOLD:

        return (
            True,
            best,
            f"semantic duplicate: {best:.4f}"
        )

    return (
        False,
        best,
        f"accepted: {best:.4f}"
    )


def create_content(existing_markdown, quote):

    # We maintain a canonical copy in the main repository.
    #
    # IMPORTANT:
    # The existing Wiki content is preserved.
    # We only add the new quote to Quote for Work
    # or Quote for Life.

    from datetime import date

    today = date.today().isoformat()

    category_heading = (
        "## Quote for your Work"
        if quote["category"] == "Work"
        else
        "## Quote for your Life"
    )

    block = (
        f"\n\n### 🌟 \"{quote['quote']}\"\n\n"
        f"— {quote['author']}\n\n"
        f"**The Source:** {quote['source_url']}\n\n"
        f"**Category:** {quote['category']}\n\n"
        f"**Added:** {today}\n\n"
    )

    # Put new quote immediately after
    # the relevant category heading.

    position = existing_markdown.find(
        category_heading
    )

    if position == -1:

        raise RuntimeError(
            f"Could not find Wiki section: "
            f"{category_heading}"
        )

    position += len(category_heading)

    return (
        existing_markdown[:position]
        +
        block
        +
        existing_markdown[position:]
    )


def main():

    print(
        "Reading existing Wiki Home...",
        file=sys.stderr
    )

    wiki_markdown = read_wiki_home()

    existing = existing_quotes(
        wiki_markdown
    )

    print(
        f"Found {len(existing)} existing quotes.",
        file=sys.stderr
    )

    for attempt in range(1, 11):

        print(
            f"Searching candidate #{attempt}...",
            file=sys.stderr
        )

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
            reason,
            file=sys.stderr
        )

        if duplicate:
            continue

        # Update canonical repository file.
        HOME.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        new_content = create_content(
            wiki_markdown,
            candidate
        )

        HOME.write_text(
            new_content,
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
        "Could not find a unique quote "
        "after 10 attempts."
    )


if __name__ == "__main__":
    main()
