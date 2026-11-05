"""Grounded answer generation. Default mode summarizes retrieved evidence; optional OpenAI mode."""
import os

FALLBACK = "Not specified in the provided policies."

def generate_answer(question, chunks, use_llm=False):
    evidence = [c for c in chunks if c.get("score", 0) >= 0.20]
    if not evidence:
        return FALLBACK, []
    citations = list(dict.fromkeys((c["source"], c["page"]) for c in evidence))
    if use_llm and os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            context = "\n".join(f'[{c["source"]}, page {c["page"]}] {c["text"]}' for c in evidence)
            response = OpenAI().chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                temperature=0,
                messages=[
                    {"role":"system","content": "Answer only from the supplied policy excerpts. If unsupported, reply exactly: Not specified in the provided policies. Distinguish superseded policy text from current policy. Cite filename and page."},
                    {"role":"user","content": f"Question: {question}\nPolicy excerpts:\n{context}"}
                ])
            answer=response.choices[0].message.content.strip()
            if not answer: answer=FALLBACK
            return answer, citations
        except Exception:
            pass
    # Transparent offline mode: return retrieved excerpts as evidence, not fabricated synthesis.
    if all(c.get("version") == "superseded" for c in evidence):
        prefix = "The retrieved policy is marked superseded: "
    else:
        prefix = "Relevant policy text: "
    return prefix + " ".join(c["text"] for c in evidence), citations
