"""Normalization helpers: phone, date, skills, country."""
import re
from typing import List


def normalize_phone(phone: str) -> str:
    if not phone:
        return None
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) > 10 and digits.startswith('1'):
        return '+' + digits
    if len(digits) >= 8:
        return '+' + digits
    return phone


def normalize_date_to_ym(date_str: str) -> str:
    # very small heuristic parser for common formats
    if not date_str:
        return None
    m = re.search(r"(\d{4})[-/](\d{1,2})", date_str)
    if m:
        y, mo = m.group(1), int(m.group(2))
        return f"{y}-{mo:02d}"
    m = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})", date_str)
    if m:
        a, b, c = m.group(1), m.group(2), m.group(3)
        if len(c) == 2:
            c = '20' + c
        return f"{c}-{int(a):02d}"
    return None


SKILL_ALIASES = {
    "py": "python",
    "python3": "python",
    "js": "javascript",
}


def normalize_skills(skills) -> List[str]:
    if not skills:
        return []
    out = []
    if isinstance(skills, str):
        parts = re.split(r"[,;|]", skills)
    else:
        parts = skills
    for p in parts:
        s = p.strip().lower()
        if not s:
            continue
        s = SKILL_ALIASES.get(s, s)
        out.append(s)
    return sorted(set(out))


COUNTRY_MAP = {"united states": "US", "usa": "US", "us": "US"}


def normalize_country(country: str) -> str:
    if not country:
        return None
    c = country.strip().lower()
    return COUNTRY_MAP.get(c, c.upper()[:2])
