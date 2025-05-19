import re

def ats_check_basic(text, keywords):
    suggestions, checklist = [], {}
    score = 100
    clean = text.lower()
    normalized = re.sub(r'\s+', '', clean)

    if not re.search(r'\+?\d{10}', clean):
        suggestions.append("Add a valid phone number")
        checklist["Phone"] = False
        score -= 10
    else:
        checklist["Phone"] = True

    if not re.search(r'\S+@\S+\.\S+', clean):
        suggestions.append("Add a professional email")
        checklist["Email"] = False
        score -= 10
    else:
        checklist["Email"] = True

    if "linkedin" not in clean:
        suggestions.append("Add your LinkedIn link")
        checklist["LinkedIn"] = False
        score -= 5
    else:
        checklist["LinkedIn"] = True

    if "github" not in clean:
        suggestions.append("Consider adding GitHub if you're a developer")
        checklist["GitHub"] = False
    else:
        checklist["GitHub"] = True

    verbs = ["developed", "built", "created", "led"]
    if not any(v in clean for v in verbs):
        suggestions.append("Use action verbs like 'developed', 'led'")
        checklist["Action Verbs"] = False
        score -= 10
    else:
        checklist["Action Verbs"] = True

    if not re.search(r'\b\d+%?|\$\d+|\d+k\b', clean):
        suggestions.append("Add quantified achievements (like %, $, numbers)")
        checklist["Quantified Impact"] = False
        score -= 5
    else:
        checklist["Quantified Impact"] = True

    missing = [k for k in keywords if k.lower() not in clean]
    if missing:
        suggestions.append("Missing keywords: " + ", ".join(missing[:5]))
        checklist["Keywords"] = False
        score -= min(20, len(missing)*2)
    else:
        checklist["Keywords"] = True

    return max(score, 0), suggestions, checklist