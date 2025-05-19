# 📋 AI Resume Analyzer (with ATS + Job Fit Scoring)

This is a fully modular, AI-powered resume analyzer web app built with **Streamlit**. It performs ATS compliance checks, extracts keywords from job descriptions, and uses **Hugging Face's zero-shot classification** to assess how well a resume aligns with a target job.

---

## 🚀 Features

- ✅ ATS Compliance Evaluation (contact info, structure, action verbs, metrics)
- 🤖 AI-based Job Role Relevance Scoring
- 🧠 Keyword Extraction from Job Descriptions
- 📄 PDF Report Generation
- 🧩 Modular Codebase for Easy Expansion

---

## 📁 Folder Structure

```
resume-analyzer/
├── app.py                      # Main Streamlit UI
├── .env                        # Contains Hugging Face API token
├── utils/
│   ├── __init__.py             # Optional
│   ├── parser.py               # PDF text extraction
│   ├── keyword_extraction.py   # Extract keywords from JD
│   ├── ats_check_basic.py      # Rule-based ATS evaluation
│   ├── ai_alignment_check.py   # AI job-role relevance scoring
│   ├── analyze_resume.py       # Combines basic + AI checks
│   ├── pdf_generator.py        # PDF report creation
```

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 3. Install dependencies

If you have a `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

Otherwise, install manually:

```bash
pip install streamlit transformers PyPDF2 fpdf python-dotenv
```

### 4. Add Hugging Face API key

Create a `.env` file in the root directory:

```env
HUGGINGFACE_API_TOKEN=your_actual_token_here
```

> 🔑 You can get a free token from https://huggingface.co/settings/tokens

### 5. Run the app

```bash
streamlit run app.py
```

Then open your browser and go to: http://localhost:8501

---

[//]: # (## 📷 Screenshot)

[//]: # ()
[//]: # (_&#40;Insert a screenshot of the app in use here if available&#41;_)

[//]: # ()
[//]: # (---)

## 📌 Future Improvements

- [ ] Add OCR support for image-based PDFs
- [ ] Integrate AI-based rephrasing for experience lines
- [ ] Support `.docx` file uploads
- [ ] Export enhanced resume suggestions as `.docx`

---

## 📄 License

MIT License — free for personal and commercial use.

---

## 🙋 Support

Open an issue or contact [shubhamotsav@gmail.com](mailto:shubhamotsav@gmail.com)
