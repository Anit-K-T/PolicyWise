
import os

FALLBACK = "Not specified in the provided policies."


def generate_answer(question, chunks, use_llm=False):

    if not chunks:
        return FALLBACK, []

    citations = list(dict.fromkeys(
        (c["source"], c["page"])
        for c in chunks
    ))

    if use_llm and os.getenv("OPENAI_API_KEY"):

        try:
            from openai import OpenAI

            context = "\n\n".join(
                f"[{c['source']}, page {c['page']}, "
                f"status: {c.get('status', 'unknown')}]\n"
                f"{c['text']}"
                for c in chunks
            )

            response = OpenAI().chat.completions.create(
                model=os.getenv(
                    "OPENAI_MODEL",
                    "gpt-4o-mini"
                ),
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer using only the supplied policy "
                            "evidence. Do not invent facts or citations. "
                            "If the evidence does not answer the question, "
                            f"reply exactly: {FALLBACK} "
                            "Distinguish current and superseded policies. "
                            "Cite the source filename and page."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Question: {question}\n\n"
                            f"Evidence:\n{context}"
                        )
                    }
                ]
            )

            answer = response.choices[0].message.content

            if not answer:
                return FALLBACK, []

            return answer.strip(), citations

        except Exception:
            pass

    # Offline mode: display evidence without pretending
    # that an LLM has synthesized an answer.

    evidence_text = "\n\n".join(
        f"{c['text']} ({c['source']}, page {c['page']})"
        for c in chunks
    )

    return (
        "Relevant retrieved policy evidence:\n\n" + evidence_text,
        citations
    )
