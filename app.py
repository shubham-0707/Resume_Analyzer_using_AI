import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.keyword_extraction import extract_keywords
from utils.analyze_resume import analyze_resume
from utils.pdf_generator import generate_pdf_report

st.set_page_config(page_title="All-in-One Resume Analyzer", layout="centered")
st.title("📋 AI Resume Analyzer with ATS Checker")

st.subheader("📋 Resume Input")
resume_text_input = st.text_area("Paste your resume text here (optional, if no PDF upload):", height=150)
file = st.file_uploader("📤 Or upload your resume (PDF)", type=["pdf"])

st.subheader("🎯 Target Job Role")
job = st.text_input("Enter the target job role:")

st.subheader("📝 Job Description")
job_description = st.text_area("Paste the job description to extract keywords:", height=200)

keywords_input = st.text_input("🧠 Important keywords (comma separated)")
if job_description and not keywords_input:
    extracted = extract_keywords(job_description)
    keywords_input = ", ".join(extracted)
    st.info(f"Extracted: {keywords_input}")

if job and keywords_input and (file or resume_text_input):
    with st.spinner("Analyzing your resume..."):
        text = extract_text_from_pdf(file) if file else resume_text_input
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

        result = analyze_resume(text, keywords, job, job_description)

        st.subheader("📊 Summary")
        st.success(f"AI Job Match: {result['alignment_label']} ({result['alignment_score']:.2%})")
        st.info(f"ATS Score: {result['ats_score']}/100")

        st.subheader("✅ Checklist")
        for item, ok in result['checklist'].items():
            st.write("✅" if ok else "❌", item)

        st.subheader("🛠 Suggestions")
        for tip in result['suggestions']:
            st.write("-", tip)

        st.subheader("📄 Resume Text")
        st.text_area("Extracted Text", text, height=300)

        pdf = generate_pdf_report(result['ats_score'], (result['alignment_label'], result['alignment_score']), result['suggestions'])
        st.download_button("📥 Download Report", data=pdf, file_name="resume_report.pdf")
else:
    st.info("👆 Fill all fields and upload your resume to begin.")