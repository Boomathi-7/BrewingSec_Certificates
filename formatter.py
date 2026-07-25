import re

# Known acronyms and custom-cased college/org names
ACRONYMS = {
    "kgisl": "KGiSL",
    "kite": "KITE",
    "psg": "PSG",
    "iit": "IIT",
    "nit": "NIT",
    "srm": "SRM",
    "bits": "BITS",
    "vit": "VIT",
    "amrita": "Amrita",
    "rmd": "RMD",
    "rmk": "RMK",
    "sns": "SNS",
    "srec": "SREC",
    "skcet": "SKCET",
    "skct": "SKCT",
    "sastra": "SASTRA",
    "mit": "MIT",
    "gct": "GCT",
    "tcs": "TCS",
    "cts": "CTS",
    "cse": "CSE",
    "ece": "ECE",
    "eee": "EEE",
    "mech": "MECH",
    "civil": "CIVIL",
    "aids": "AI & DS",
    "ai&ds": "AI & DS",
    "it": "IT",
}

# Words that should be lowercase in titles unless at start/end
LOWERCASE_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "via", "with", "&"
}


def format_participant_name(raw_name: str) -> str:
    """Format participant name with pro UI standards:
    - Normalizes whitespace
    - Title cases words, handling hyphens, apostrophes, and initials
    - Uppercases single letter initials and Roman numerals
    
    Examples:
        "boomathi p" -> "Boomathi P"
        "m. john doe" -> "M. John Doe"
        "mary-jane o'connor" -> "Mary-Jane O'Connor"
    """
    if not raw_name:
        return ""
    
    # Clean up whitespace
    cleaned = re.sub(r'\s+', ' ', raw_name.strip())
    words = cleaned.split(' ')
    formatted_words = []

    for idx, word in enumerate(words):
        # Check for hyphenated words
        if '-' in word:
            parts = word.split('-')
            formatted_word = '-'.join(p.capitalize() for p in parts)
        # Check for apostrophe (e.g. O'Connor)
        elif "'" in word:
            parts = word.split("'")
            formatted_word = "'".join(p.capitalize() for p in parts)
        # Check for initials with dot (e.g. "m." or "p.")
        elif re.match(r'^[a-zA-Z]\.$', word):
            formatted_word = word.upper()
        # Single letter initial (e.g. "p")
        elif len(word) == 1 and word.isalpha():
            formatted_word = word.upper()
        # Roman numerals (e.g. "iii", "iv")
        elif word.lower() in ("i", "ii", "iii", "iv", "v", "vi"):
            formatted_word = word.upper()
        else:
            formatted_word = word.capitalize()

        formatted_words.append(formatted_word)

    return " ".join(formatted_words)


def format_college_name(raw_college: str) -> str:
    """Format college/institution name like a pro UI developer:
    - Preserves known acronyms (KGiSL, PSG, IIT, etc.)
    - Properly title-cases words (lowercasing 'of', 'and', 'for', etc. inside sentence)
    - Expands common abbreviations (Inst. -> Institute, Tech. -> Technology)
    
    Examples:
        "kgisl institute of technology" -> "KGiSL Institute of Technology"
        "sri krishna college of engineering and technology" -> "Sri Krishna College of Engineering and Technology"
    """
    if not raw_college:
        return ""

    # Clean whitespace
    cleaned = re.sub(r'\s+', ' ', raw_college.strip())
    
    # Common abbreviation replacements
    replacements = {
        r'\binst\.(?=\s|$)': 'Institute',
        r'\bcoll\.(?=\s|$)': 'College',
        r'\btech\.(?=\s|$)': 'Technology',
        r'\bengg\.(?=\s|$)': 'Engineering',
        r'\buniv\.(?=\s|$)': 'University',
        r'\bdept\.(?=\s|$)': 'Department of',
    }
    for pattern, repl in replacements.items():
        cleaned = re.sub(pattern, repl, cleaned, flags=re.IGNORECASE)

    words = cleaned.split(' ')
    total_words = len(words)
    formatted_words = []

    for idx, word in enumerate(words):
        word_lower = word.lower()
        clean_word_lower = re.sub(r'[^\w]', '', word_lower)

        # Check if known acronym
        if clean_word_lower in ACRONYMS:
            # Preserve punctuation if present
            acronym_val = ACRONYMS[clean_word_lower]
            formatted_word = word.lower().replace(clean_word_lower, acronym_val)
        # Minor words stay lowercase unless at beginning or end of name
        elif word_lower in LOWERCASE_WORDS and idx > 0 and idx < total_words - 1:
            formatted_word = word_lower
        # Hyphenated
        elif '-' in word:
            parts = word.split('-')
            formatted_word = '-'.join(p.capitalize() for p in parts)
        # General Title Case
        else:
            formatted_word = word.capitalize()

        formatted_words.append(formatted_word)

    return " ".join(formatted_words)
