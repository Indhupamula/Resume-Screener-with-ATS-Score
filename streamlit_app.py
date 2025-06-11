import streamlit as st
import os
import pandas as pd
from analyzer import *

# ✅ Set OpenAI API Key from Streamlit Secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
gpt_key = os.environ["OPENAI_API_KEY"]

# ✅ Upload Job Description
uploaded_JD = st.file_uploader("Upload the Job Description", type=['pdf', 'docx', 'txt'])

# ✅ Upload Resumes (Multiple)
uploaded_resumes = st.file_uploader("Upload Resumes", accept_multiple_files=True, type=['pdf', 'docx'])

# ✅ Trigger Analysis
if uploaded_JD and uploaded_resumes:
    if st.button("Analyze"):
        result_list = []

        with st.spinner(text="Analyzing..."):
            # Process JD
            jd_file, uploaded_JD_type = file_create(uploaded_JD, "job_description")
            jd_content = extract_text(jd_file, uploaded_JD_type)
            jd_format = format_content(jd_content, gpt_key)

            # Process each resume
            for resume in uploaded_resumes:
                resume_file, resume_type = file_create(resume, "resume")
                resume_content = extract_text(resume_file, resume_type)
                resume_format = format_content(resume_content, gpt_key)

                # Compare JD and Resume
                applicant_eligibility = elibility_check(jd_format, resume_format, gpt_key)
                response = analyze_jd_resume(jd_format, resume_format, applicant_eligibility, gpt_key)
                json_data = response
                result_list.extend(json_data)

        # Convert and show final results
        final_result = convert_to_dataframe(result_list)
        st.write(final_result)
