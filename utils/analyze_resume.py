from utils.ats_check_basic import ats_check_basic
from utils.ai_alignment_check import ai_alignment_check

def analyze_resume(text, keywords, job, job_desc=None):
    ats_score, suggestions, checklist = ats_check_basic(text, keywords)
    fit_label, fit_score = ai_alignment_check(text, job, job_desc)
    return {
        "ats_score": ats_score,
        "suggestions": suggestions,
        "checklist": checklist,
        "alignment_label": fit_label,
        "alignment_score": fit_score
    }