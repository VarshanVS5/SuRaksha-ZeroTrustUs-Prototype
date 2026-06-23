import pdfplumber
from pathlib import Path

from app.utils import (
    clean_text,
    generate_document_id,
)


class PDFIngestor:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_text(self) -> str:
        markdown_parts = []

        with pdfplumber.open(self.file_path) as pdf:

            for page_number, page in enumerate(pdf.pages, start=1):

                text = page.extract_text() or ""

                text = clean_text(text)

                markdown_parts.append(
                    f"\n\n## Page {page_number}\n\n{text}"
                )

                tables = page.extract_tables()

                if tables:
                    markdown_parts.append(
                        self.tables_to_markdown(tables)
                    )

        return "\n".join(markdown_parts)

    def tables_to_markdown(self, tables) -> str:
        output = []

        for table in tables:

            if not table:
                continue

            rows = [
                [
                    str(cell).strip() if cell is not None else ""
                    for cell in row
                ]
                for row in table
            ]

            if len(rows) < 2:
                continue

            header = rows[0]

            output.append("\n### Table\n")

            output.append(
                "| " + " | ".join(header) + " |"
            )

            output.append(
                "| " + " | ".join(["---"] * len(header)) + " |"
            )

            for row in rows[1:]:
                output.append(
                    "| " + " | ".join(row) + " |"
                )

            output.append("\n")

        return "\n".join(output)

    def extract_title(self) -> str:

        with pdfplumber.open(self.file_path) as pdf:

            if not pdf.pages:
                return Path(self.file_path).stem

            first_page = pdf.pages[0]

            text = first_page.extract_text() or ""

            lines = [
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ]

            if lines:
                return lines[0]

        return Path(self.file_path).stem

    def process(self):

        markdown = self.extract_text()

        return {
            "document_id": generate_document_id(
                self.file_path
            ),
            "title": self.extract_title(),
            "raw_markdown": markdown,
        }