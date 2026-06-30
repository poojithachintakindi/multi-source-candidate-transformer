"""Detect source type from filename or content."""
import os


def detect_source(path: str, content: bytes = None) -> str:
    _, ext = os.path.splitext(path.lower())
    if ext == ".csv":
        return "recruiter_csv"
    if ext == ".json":
        return "ats_json"
    if ext in (".txt", ""):
        # heuristics: short JSON-like -> ats_json
        if content:
            s = content.strip()
            if s.startswith(b"{") or s.startswith(b"["):
                return "ats_json"
        return "text"
    return "unknown"
