import json
import os
import sys
import tempfile
import traceback

import streamlit as st

sys.path.append(os.getcwd())

from app.main import process_claim

st.set_page_config(page_title="FNOL Claims Agent", layout="wide")

st.title("🧾 Autonomous Insurance Claims Agent")
st.write("Upload an FNOL PDF to extract fields and route the claim.")

# Session state init
if "result" not in st.session_state:
    st.session_state.result = None

if "uploaded_path" not in st.session_state:
    st.session_state.uploaded_path = None

uploaded_file = st.file_uploader("Upload FNOL PDF", type=["pdf"])

if uploaded_file:
    st.write("Selected:", uploaded_file.name)

    # Save file once
    if st.session_state.uploaded_path is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            st.session_state.uploaded_path = tmp.name

if st.button("Process Claim") and st.session_state.uploaded_path:
    with st.spinner("Processing..."):
        try:
            st.session_state.result = process_claim(st.session_state.uploaded_path)
        except Exception:
            st.error("Processing failed")
            st.code(traceback.format_exc())

# Display result if exists
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
