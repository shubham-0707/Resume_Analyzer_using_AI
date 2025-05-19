from transformers import pipeline
import re
import os
from dotenv import load_dotenv

load_dotenv()
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", token=os.getenv("HUGGINGFACE_API_TOKEN"))

def ai_alignment_check(resume_text, job_role, job_description=None):
    text = re.sub(r'\s+', ' ', resume_text.strip())
    target = job_description or f"Resume for {job_role}"
    labels = [f"Highly suitable for {job_role}", f"Partially suitable for {job_role}", f"Not suitable for {job_role}"]
    result = classifier(text, labels)
    return result['labels'][0], result['scores'][0]