#!/usr/bin/env python
"""Quick retrieval sanity check of the finished index (NOT the final retrieval layer).

For each question in data/G1_questions.jsonl it shows the top-3 chunks and checks
whether the expected source PDF appears in them (a simple Recall@3).
Usage:  python scripts/sanity_check.py [--index-dir index] [--query "free text"]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ingestion import VectorStore, get_embedder  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index-dir", default="index")
    ap.add_argument("--questions", default="data/G1_questions.jsonl")
    ap.add_argument("--query", help="run one free-text query instead of the question file")
    ap.add_argument("-k", type=int, default=3)
    args = ap.parse_args()

    store = VectorStore.load(args.index_dir)
    embedder = get_embedder("hash" if store.meta.get("embedder", "").startswith("hashing") else "minilm")
    if embedder.name != store.meta.get("embedder"):
        sys.exit(f"Index was built with {store.meta.get('embedder')} but loaded {embedder.name}")

    def show(q: str):
        hits = store.search(embedder.encode([q])[0], args.k)
        for rank, (score, c) in enumerate(hits, 1):
            snippet = " ".join(c["text"].split())[:70]
            print(f"   {rank}. {score:.3f}  {c['doc_name']} p{c['page']} [{c['status']}] {snippet}...")
        return hits

    if args.query:
        show(args.query)
        return

    ok = total = 0
    for line in Path(args.questions).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        print(f"\nQ: {item['question']}   (expected source: {item['source']})")
        hits = show(item["question"])
        if item["source"] == "none":
            print("   -> no source expected; the answer layer must abstain "
                  f"(top score {hits[0][0]:.3f}).")
            continue
        total += 1
        found = any(c["doc_name"] == item["source"] for _, c in hits)
        ok += found
        print(f"   -> source in top-{args.k}: {'YES' if found else 'NO'}")
    print(f"\nRecall@{args.k} on questions with a source: {ok}/{total}")


if __name__ == "__main__":
    main()
