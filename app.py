import streamlit as st

st.set_page_config(
    page_title="PolicyWise",
    page_icon="📘",
    layout="centered"
)

st.title("📘 PolicyWise")
st.subheader("Source-Grounded HR Policy Assistant")

st.write(
    "Ask questions about company HR policies and receive "
    "answers grounded in the provided policy documents."
)

st.divider()

st.markdown("### Ask an HR Policy Question")

question = st.text_area(
    "Enter your question:",
    placeholder="Example: How many annual leave days are employees entitled to?",
    height=100
)

if st.button("Get Answer", type="primary"):
    if question.strip():
        st.info("Your question will be processed using the HR policy documents.")
        st.warning("Backend integration is pending.")
    else:
        st.warning("Please enter a question.")

st.divider()

with st.expander("About PolicyWise"):
    st.write(
        "PolicyWise is a Retrieval-Augmented Generation (RAG) "
        "assistant designed to answer employee questions using "
        "official HR policy documents, with source references."
    )
