
import streamlit as st

st.set_page_config(
    page_title="PolicyWise",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PolicyWise")
st.subheader("Source-Grounded HR Policy Assistant")

st.write(
    "Ask questions about company HR policies "
    "and get reliable answers with document references."
)

st.divider()

question = st.text_input(
    "Enter your HR policy question:",
    placeholder="Example: What is the annual leave policy?"
)

if st.button("Get Answer", type="primary"):
    if question.strip():
        st.info("Your question will be processed by the RAG pipeline.")
    else:
        st.warning("Please enter a question.")

st.sidebar.title("About PolicyWise")
st.sidebar.write(
    "An AI-powered HR assistant that answers "
    "questions using provided policy documents."
)
