import re
from pathlib import Path


def generate_document_id(file_path: str) -> str:
    name = Path(file_path).stem.upper()

    name = re.sub(r"[^A-Z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name)

    return name


def normalize_whitespace(text: str) -> str:
    text = re.sub(r"\r", "", text)
    text = re.sub(r"\t", " ", text)
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def remove_page_numbers(text: str) -> str:
    patterns = [
        r"(?im)^page\s+\d+\s*$",
        r"(?im)^page\s+\d+\s+of\s+\d+\s*$",
        r"(?im)^\d+\s*$",
    ]

    for pattern in patterns:
        text = re.sub(pattern, "", text)

    return text


def remove_common_headers_footers(text: str) -> str:
    patterns = [
        r"(?im)^reserve bank of india.*$",
        r"(?im)^www\.rbi\.org\.in.*$",
        r"(?im)^rbi\/.*$",
        r"(?im)^master direction.*$",
    ]

    for pattern in patterns:
        text = re.sub(pattern, "", text)

    return text


def clean_text(text: str) -> str:
    text = remove_page_numbers(text)
    text = remove_common_headers_footers(text)
    text = normalize_whitespace(text)

    return text