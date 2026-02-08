import json
import os
import tempfile
import traceback

import streamlit as st

from app.main import process_claim

st.set_page_config(page_title="FNOL Claims Agent", layout="wide")

st.title(" Autonomous Insurance Claims Agent")
st.write("Upload an FNOL PDF to extract fields and route the claim.")

if "result" not in st.session_state:
    st.session_state.result = None

uploaded_file = st.file_uploader("Upload FNOL PDF", type=["pdf"])

if uploaded_file:
    st.write("Selected:", uploaded_file.name)

if st.button("Process Claim") and uploaded_file:
    if not os.getenv("GEMINI_API_KEY"):
        st.error('GEMINI_API_KEY is missing. Run: export GEMINI_API_KEY="YOUR_KEY"')
    else:
        with st.spinner("Processing..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    temp_path = tmp.name

                st.session_state.result = process_claim(temp_path)

            except Exception:
                st.error("Processing failed")
                st.code(traceback.format_exc())

if st.session_state.result:
    result = st.session_state.result

    st.success("Processing complete")

    st.subheader("Extracted Fields")
    st.json(result["extractedFields"])

    st.subheader("Missing Fields")
    st.write(result["missingFields"])

    st.subheader("Route")
    st.write(result["recommendedRoute"])

    st.subheader("Reasoning")
    st.write(result["reasoning"])

    st.download_button("Download JSON", json.dumps(result, indent=2), "claim.json")
