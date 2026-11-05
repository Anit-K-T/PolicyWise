
import streamlit as st
import json
from pathlib import Path

from src.retrieval import PolicyRetriever
from src.answer_generator import generate_answer, FALLBACK

st.set_page_config(page_title="PolicyWise", page_icon="📘", layout="centered")

st.title("📘 PolicyWise")
st.subheader("Source-Grounded HR Policy Assistant")
st.write("Ask questions about company HR policies and receive answers grounded in the provided policy documents.")

index_file = Path("index/chunks.jsonl")

if not index_file.exists():
    st.error("Policy index not found. Please run the ingestion pipeline first.")
    st.stop()

with index_file.open("r", encoding="utf-8") as file:
    chunks = [json.loads(line) for line in file if line.strip()]

for chunk in chunks:
    chunk["source"] = chunk["doc_name"]
    chunk["version"] = chunk["status"]

retriever = PolicyRetriever(chunks)

st.divider()
st.markdown("### Ask an HR Policy Question")

question = st.text_area(
    "Enter your question:",
    placeholder="Example: What is the hotel limit for Tier 1 cities?",
    height=100
)

if st.button("Get Answer", type="primary"):
    if question.strip():
        results = retriever.retrieve(question, k=3)

        current_results = [
            item for item in results
            if item.get("status") == "current"
        ]

        # Prefer current policies when available.
        selected = current_results if current_results else results

        answer, citations = generate_answer(question, selected)

        st.markdown("### Answer")
        st.write(answer)

        if citations:
            st.markdown("### Sources")
            for source, page in citations:
                st.write(f"- {source}, Page {page}")
        else:
            st.info(FALLBACK)
    else:
        st.warning("Please enter a question.")

st.divider()

with st.expander("About PolicyWise"):
    st.write(
        "PolicyWise is a Retrieval-Augmented Generation (RAG) "
        "assistant that answers employee questions using official "
        "HR policy documents and provides source references."
    )
