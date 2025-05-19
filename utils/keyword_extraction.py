import string
from collections import Counter

def extract_keywords(text, top_n=20):
    stopwords = set(["and", "or", "the", "to", "of", "in", "with", "for", "on", "is", "are", "a", "an"])
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    words = [w for w in text.split() if w not in stopwords and len(w) > 2]
    return [w for w, _ in Counter(words).most_common(top_n)]