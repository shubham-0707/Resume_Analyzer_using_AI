# Resume Analyzer Application

This is a comprehensive resume analysis tool built with Streamlit that helps job seekers optimize their resumes for both ATS (Applicant Tracking Systems) and human reviewers.

## Features

- **Resume Text Extraction**: Extract text from PDF resumes
- **ATS Compatibility Check**: Score resumes based on ATS-friendly criteria
- **Keyword Analysis**: Match resume content against job requirements
- **AI Job Match Scoring**: Use AI to evaluate overall job fit
- **Automatic Keyword Extraction**: Extract keywords from job descriptions
- **PDF Report Generation**: Download comprehensive analysis reports

## Project Structure

```
resume_analyzer/
├── main.py               # Main Streamlit application
├── pdf_utils.py          # PDF handling utilities
├── ats_analyzer.py       # ATS compatibility checking
├── ai_scorer.py          # AI-based job fit scoring
├── keyword_extractor.py  # Job description keyword extraction
├── .env                  # Environment variables (HuggingFace API token)
└── ats_resume_template.docx  # Downloadable resume template
```

## Requirements

- Python 3.8+
- Streamlit
- PyPDF2
- fpdf
- transformers
- python-dotenv
- huggingface-hub

## Environment Setup

1. Install dependencies:
   ```
   pip install streamlit PyPDF2 fpdf transformers python-dotenv huggingface-hub
   ```

2. Create a `.env` file with your HuggingFace API token:
   ```
   HUGGINGFACE_API_TOKEN=your_token_here
   ```

## Running the Application

```
streamlit run main.py
```

## How to Use

1. **Manual Keywords**: Enter job role and keywords manually
2. **Auto-Extract Keywords**: Paste a full job description to automatically extract keywords
3. Upload your resume (PDF format)
4. Review analysis results and suggestions
5. Download the analysis report as PDF
6. Download an ATS-friendly resume template if needed