import streamlit as st
import PyPDF2
import re
from transformers import pipeline
from fpdf import FPDF
import os
from dotenv import load_dotenv
from io import BytesIO
from collections import Counter
import string

# Load API key
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

st.set_page_config(page_title="All-in-One Resume Analyzer", layout="centered")

st.title("📋 AI Resume Analyzer with ATS Checker")
st.write("Upload your resume, enter your target job, paste the job description, and get a full analysis — no other tools needed.")

# ----------------- Extract Text -------------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page_text := page.extract_text():
            text += page_text + "\n"
    return text.strip()

# ----------------- Keyword Extraction -------------------
def extract_keywords(text, top_n=20):
    stopwords = set([
        "and", "or", "but", "the", "a", "an", "with", "for", "to", "of",
        "in", "on", "at", "by", "from", "as", "is", "are", "was", "were",
        "this", "that", "these", "those", "it", "its", "be", "has", "have",
        "will", "can", "may", "should", "you", "your", "i", "we", "they"
    ])
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = [word for word in text.split() if word not in stopwords and len(word) > 2]
    counter = Counter(words)
    common = counter.most_common(top_n)
    return [word for word, _ in common]

# ----------------- ATS Evaluation -------------------
def clean_text(text):
    return text.replace('\n', ' ').replace('\u200b', '').strip().lower()

def ats_check(text, keywords):
    suggestions, checklist = [], {}
    score = 100

    clean = clean_text(text)
    normalized = re.sub(r'[\s\n]+', '', text.lower())  # remove line breaks and whitespace
    plain = text.lower()

    # Phone
    phone_match = re.search(r'(\+91[-\s]?)?\d{10}', clean)
    if not phone_match:
        suggestions.append("📱 Add a valid phone number with or without country code.")
        checklist["Phone number"] = False
        score -= 10
    else:
        checklist["Phone number"] = True

    # Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', clean)
    if not email_match:
        suggestions.append("📧 Add a professional email address.")
        checklist["Email"] = False
        score -= 10
    else:
        checklist["Email"] = True

    # LinkedIn (URL or mention)
    if "linkedin.com/in" in normalized or "linkedin" in plain:
        checklist["LinkedIn"] = True
    else:
        suggestions.append("🔗 Add your LinkedIn profile link or mention.")
        checklist["LinkedIn"] = False
        score -= 5

    # GitHub (URL or mention)
    if "github.com" in normalized or "github" in plain:
        checklist["GitHub"] = True
    else:
        suggestions.append("💻 Add your GitHub link or username.")
        checklist["GitHub"] = False

    # Action verbs
    verbs = ["developed", "built", "created", "led", "managed", "designed"]
    if not any(verb in clean for verb in verbs):
        suggestions.append("🛠 Use strong action verbs like 'developed', 'led', or 'built'.")
        checklist["Action verbs"] = False
        score -= 10
    else:
        checklist["Action verbs"] = True

    # Format
    if re.search(r'<table|column|two-column', clean):
        suggestions.append("🧱 Avoid tables or columns — not ATS friendly.")
        checklist["ATS-safe format"] = False
        score -= 5
    else:
        checklist["ATS-safe format"] = True

    # Keywords
    missing = [kw for kw in keywords if kw.lower() not in clean]
    if missing:
        suggestions.append(f"📌 Add missing keywords: {', '.join(missing[:5])}")
        checklist["Relevant keywords"] = False
        score -= min(20, len(missing) * 2)
    else:
        checklist["Relevant keywords"] = True

    # Length
    if len(clean.split()) < 150:
        suggestions.append("📉 Resume is too short — add more details.")
        checklist["Sufficient content"] = False
        score -= 5
    else:
        checklist["Sufficient content"] = True

    return max(score, 0), suggestions, checklist

# ----------------- AI Relevance Score -------------------
@st.cache_resource
def load_model():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli", token=HUGGING_FACE_API_TOKEN)

model = load_model()

def get_fit_score(text, role):
    labels = [f"Highly suitable for {role}", f"Partially suitable for {role}", f"Not suitable for {role}"]
    result = model(text, labels)
    return result['labels'][0], result['scores'][0]

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# ----------------- PDF Report Generator -------------------
def generate_pdf_report(score, fit, suggestions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Resume Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(180, 10, f"AI Job Match: {fit[0]} ({fit[1]*100:.1f}%)")
    pdf.multi_cell(180, 10, f"ATS Score: {score}/100")
    pdf.ln(5)

    pdf.cell(0, 10, "Suggestions:", ln=True)
    for tip in suggestions:
        clean_tip = remove_emojis(tip)
        pdf.multi_cell(180, 10, f"- {clean_tip}")

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# ----------------- UI -------------------
st.subheader("📋 Resume Input")
resume_text_input = st.text_area("Paste your resume text here (optional, if no PDF upload):", height=150)
file = st.file_uploader("📤 Or upload your resume (PDF)", type=["pdf"])

st.subheader("🎯 Target Job Role")
job = st.text_input("Enter the target job role:")

st.subheader("📝 Job Description (Paste here)")
job_description = st.text_area("Paste the full job description to extract keywords and analyze fit:", height=200)

keywords_input = st.text_input("🧠 Important keywords (comma separated) - will be auto-filled from job description")

# Auto keyword extraction
if job_description and not keywords_input:
    extracted_keywords = extract_keywords(job_description)
    keywords_str = ", ".join(extracted_keywords)
    st.info(f"Extracted keywords from job description: {keywords_str}")
    keywords_input = st.text_input("🧠 Important keywords (comma separated)", value=keywords_str)

# Trigger analysis
if job and keywords_input and (file or resume_text_input):
    with st.spinner("Analyzing your resume..."):
        resume_text = extract_text_from_pdf(file) if file else resume_text_input.strip()
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
        ats_score, suggestions, checklist = ats_check(resume_text, keywords)
        fit_label, fit_score = get_fit_score(resume_text, job)

        st.subheader("📊 Summary")
        st.success(f"**AI Job Match**: {fit_label} ({fit_score:.2%})")
        st.info(f"**ATS Score**: {ats_score}/100")

        st.subheader("✅ Resume Quality Checklist")
        for item, status in checklist.items():
            st.write("✅" if status else "❌", item)

        st.subheader("🛠️ Suggestions to Improve")
        for tip in suggestions:
            st.write("-", tip)

        st.subheader("📄 Resume Preview")
        st.text_area("Extracted Resume Text", resume_text, height=300)

        # Download report
        report_pdf = generate_pdf_report(ats_score, (fit_label, fit_score), suggestions)
        st.download_button("📥 Download Analysis Report (PDF)", data=report_pdf, file_name="resume_report.pdf")
else:
    st.info("👆 Enter job info, keywords, and upload or paste your resume to get started.")
