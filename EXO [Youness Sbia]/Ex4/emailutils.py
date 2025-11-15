from pathlib import Path
import re

EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')

def is_valid_email(email: str) -> bool:
    return EMAIL_RE.fullmatch(email.strip()) is not None

def extract_domain(email: str) -> str:
    return email.split('@', 1)[1]

def extract_username(email: str) -> str:
    return email.split('@', 1)[0]

def find_emails_in_file(path: Path) -> list[str]:
    emails: list[str] = []
    with open(path, 'rt') as f:
        for line in f:
            for word in line.split():
                candidate = word.strip(".,;:!?()[]{}<>\"'")
                candidate = candidate.lower()
                if is_valid_email(candidate) and candidate not in emails:
                    emails.append(candidate)
    return emails