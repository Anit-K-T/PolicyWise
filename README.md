

# PolicyWise — Group 1

A runnable HR-policy RAG prototype using the four Group 1 policy PDFs. It extracts page-level text, chunks it, retrieves the top 3 relevant passages, and displays source filename/page citations. Unanswerable queries use the required fallback.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open the local Streamlit URL. The default works without an API key. It returns source excerpts as grounded evidence. To enable synthesized answers, copy `.env.example` to `.env`, set `OPENAI_API_KEY`, export the variables in your shell, and tick the OpenAI checkbox in the sidebar.

## Architecture
PDFs → `src/ingestion.py` (text + page/file metadata, overlap, duplicate hash) → `src/retrieval.py` (TF-IDF similarity, top 3, current policy preference) → `src/answer_generator.py` (grounded answer / fallback + citations) → `app.py` (Streamlit UI).

## RAG Retrieval & Answer Generation

This contribution implements the retrieval and answer-generation components of the PolicyWise HR Policy RAG prototype.

### Files Updated

- `src/retrieval.py`
- `src/answer_generator.py`

### What Implemented

**1. `src/retrieval.py` — RAG Retrieval**

- Implemented TF-IDF-based similarity retrieval.
- Retrieves the top 3 relevant policy passages for a given question.
- Supports ranking based on current and superseded policy versions.
- Returns relevant chunk data, including text, source filename, page number, version, and similarity score.

**2. `src/answer_generator.py` — Answer Generation**

- Generates answers grounded in retrieved policy passages.
- Includes source filename and page citations.
- Implements a fallback response for questions that cannot be answered using the available policy documents.
- Supports optional LLM-based answer generation.

**3. `.gitignore`**

- Added rules to exclude environment files, virtual environments, cache files, and other unnecessary files from Git tracking.

**4. `requirements.txt`**

- Updated the project dependencies required for retrieval and answer generation.

### Integration

The retrieval and answer-generation modules integrate with the ingestion component through the shared chunk dictionary structure.

The implementation supports the required RAG workflow:

`Question → Retrieval → Top 3 Relevant Passages → Grounded Answer → Source Citations`

The default implementation works without an OpenAI API key. Optional LLM-based generation can be enabled when the API key is configured.

