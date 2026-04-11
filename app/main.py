import os

import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

st.set_page_config(page_title="Homeowners Policy Comparison", layout="wide")

st.markdown(
    """
    <style>
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def extract_text(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def compare_homeowners_policies(text1, text2, client):
    prompt = f"""
You are an expert at comparing homeowners insurance policies.

Compare these two homeowners insurance policies and return a clear, practical comparison for a homeowner.

Focus on:
1. Policy name / insurer
2. Dwelling coverage
3. Other structures coverage
4. Personal property coverage
5. Loss of use / additional living expenses
6. Personal liability
7. Medical payments to others
8. Deductible
9. Major exclusions or limitations
10. Endorsements or extra protections
11. Key differences
12. Which policy appears better overall and why

Keep the explanation easy to understand.
Use headings and bullet points.

Policy 1:
{text1[:6000]}

Policy 2:
{text2[:6000]}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text


st.markdown(
    "<h1 style='margin-top:0;'>Homeowners Policy Comparison</h1>",
    unsafe_allow_html=True,
)

st.write("Upload two homeowners insurance PDF policies and compare them with AI.")

col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader("Upload Homeowners Policy 1", type=["pdf"], key="file1")

with col2:
    file2 = st.file_uploader("Upload Homeowners Policy 2", type=["pdf"], key="file2")

if st.button("Compare Policies"):
    if not file1 or not file2:
        st.warning("Please upload both homeowners policy PDF files.")
    else:
        client = get_openai_client()

        if client is None:
            st.error("Missing OPENAI_API_KEY environment variable.")
            st.stop()

        with st.spinner("Reading policy PDFs..."):
            text1 = extract_text(file1)
            text2 = extract_text(file2)

        if not text1 or not text2:
            st.error("Could not extract text from one or both PDFs.")
            st.stop()

        with st.spinner("Comparing homeowners policies..."):
            result = compare_homeowners_policies(text1, text2, client)

        st.subheader("Comparison Result")
        st.write(result)

        st.download_button(
            label="Download Comparison",
            data=result,
            file_name="homeowners_policy_comparison.txt",
            mime="text/plain",
        )