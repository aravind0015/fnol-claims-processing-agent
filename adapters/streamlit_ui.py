import json
import tempfile

import streamlit as st

from app.main import process_claim

st.set_page_config(page_title="FNOL Claims Agent", layout="wide")

st.title("🧾 Autonomous Insurance Claims Agent")
st.write("Upload an FNOL PDF to extract fields and route the claim.")

uploaded_file = st.file_uploader("Upload FNOL PDF", type=["pdf"])

if uploaded_file is not None:
    if st.button("Process Claim"):
        with st.spinner("Processing claim..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                temp_path = tmp.name

            result = process_claim(temp_path)

        st.success("Processing complete")

        st.subheader("📦 Extracted Fields")
        st.json(result["extractedFields"])

        st.subheader("⚠️ Missing Fields")
        st.write(result["missingFields"])

        st.subheader("🚦 Recommended Route")
        st.markdown(f"**{result['recommendedRoute']}**")

        st.subheader("🧠 Reasoning")
        st.write(result["reasoning"])

        st.download_button(
            label="Download JSON",
            data=json.dumps(result, indent=2),
            file_name="claim_result.json",
            mime="application/json",
        )
