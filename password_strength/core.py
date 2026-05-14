import re
import string
from typing import Dict, List

COMMON_PASSWORDS = {"password", "123456", "123456789", "qwerty", "abc123", "letmein", "admin"}


def _charsets_present(pw: str) -> int:
    count = 0
    if re.search(r"[a-z]", pw):
        count += 1
    if re.search(r"[A-Z]", pw):
        count += 1
    if re.search(r"[0-9]", pw):
        count += 1
    if re.search(r"[" + re.escape(string.punctuation) + r"]", pw):
        count += 1
    return count


def _max_consecutive_run(pw: str) -> int:
    if not pw:
        return 0
    max_run = 1
    run = 1
    for i in range(1, len(pw)):
        if pw[i] == pw[i - 1]:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 1
    return max_run


def _has_sequence(pw: str, length: int = 3) -> bool:
    if len(pw) < length:
        return False
    s = pw.lower()
    for i in range(len(s) - length + 1):
        chunk = s[i : i + length]
        # check ascending sequence
        if all(ord(chunk[j + 1]) - ord(chunk[j]) == 1 for j in range(len(chunk) - 1)):
            return True
    return False


def score_password(pw: str) -> Dict:
    """Score a password from 0..100 and return a breakdown."""
    if not pw:
        return {"score": 0, "reason": "empty", "breakdown": {}, "components": {"length": {"score": 0, "classification": classify_score(0)}, "complexity": {"score": 0, "classification": classify_score(0)}}}

    length = len(pw)

    # immediate fail for very common passwords
    if pw.lower() in COMMON_PASSWORDS:
        comp_len = int(min(length, 30) / 30 * 100)
        comp_cplx = 5
        return {"score": 5, "reason": "common_password", "breakdown": {"length": length}, "components": {"length": {"score": comp_len, "classification": classify_score(comp_len)}, "complexity": {"score": comp_cplx, "classification": classify_score(comp_cplx)}}}

    # legacy-style partial scores used for breakdown
    length_score = min(length, 20) / 20 * 40

    # charset contribution (max 30)
    charsets = _charsets_present(pw)
    charset_score = (charsets / 4) * 30

    # entropy-like small bonus for length beyond 12 (kept for breakdown)
    bonus = 0
    if length >= 12:
        bonus = min((length - 12) * 2, 30)

    # penalties for breakdown
    repeat_penalty = max(0, (_max_consecutive_run(pw) - 2) * 4)
    sequence_penalty = 10 if _has_sequence(pw, 3) else 0

    # Compute component scores (0..100)
    length_component = int(min(length, 30) / 30 * 100)

    # Complexity base from charset variety
    complexity_base = (charsets / 4) * 100
    # give long passphrases a complexity-style bonus even if charset variety is low
    length_bonus_pct = min(max(0, (length - 12) * 3), 45)
    complexity_base = complexity_base + length_bonus_pct
    # map penalties to percentage terms
    repeat_penalty_pct = min(max(0, (_max_consecutive_run(pw) - 1) * 10), 60)
    sequence_penalty_pct = 20 if _has_sequence(pw, 3) else 0
    complexity_component = int(max(0, min(100, round(complexity_base - repeat_penalty_pct - sequence_penalty_pct))))

    # final score combines length and complexity with a bias toward length
    length_weight = 0.6
    complexity_weight = 0.4
    score = int(round((length_component * length_weight) + (complexity_component * complexity_weight)))

    breakdown = {
        "length_score": round(length_score, 1),
        "charset_score": round(charset_score, 1),
        "bonus": round(bonus, 1),
        "repeat_penalty": repeat_penalty,
        "sequence_penalty": sequence_penalty,
        "length": length,
        "charsets": charsets,
    }

    components = {
        "length": {"score": length_component, "classification": classify_score(length_component)},
        "complexity": {"score": complexity_component, "classification": classify_score(complexity_component)},
    }

    return {"score": score, "reason": "calculated", "breakdown": breakdown, "components": components}


def classify_score(score: int) -> str:
    if score < 20:
        return "Very Weak"
    if score < 40:
        return "Weak"
    if score < 60:
        return "Medium"
    if score < 80:
        return "Strong"
    return "Very Strong"


def suggest_improvements(pw: str) -> List[str]:
    suggestions = []
    if not pw:
        return ["Use a longer passphrase or password."]

    if len(pw) < 12:
        suggestions.append("Make it longer (12+ characters).")
    charsets = _charsets_present(pw)
    if charsets < 3:
        suggestions.append("Include a mix of lowercase, uppercase, digits, and symbols.")
    if _max_consecutive_run(pw) > 2:
        suggestions.append("Avoid repeated characters (e.g., 'aaaa').")
    if _has_sequence(pw, 3):
        suggestions.append("Avoid simple sequences like 'abc' or '123'.")
    if pw.lower() in COMMON_PASSWORDS:
        suggestions.append("Don't use a common password or dictionary word.")
    if not suggestions:
        suggestions.append("Looks good — consider using a password manager to generate and store a long passphrase.")
    return suggestions
