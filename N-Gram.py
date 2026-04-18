import re

def n_grams(text, n):
    words = re.findall(r'\w+', text.lower())
    
    if n <= 0:
        raise ValueError("n must be positive")
    if n > len(words):
        return []
    
    return [tuple(words[i:i+n]) for i in range(len(words)-n+1)]