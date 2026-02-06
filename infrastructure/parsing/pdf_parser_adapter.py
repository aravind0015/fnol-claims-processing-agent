from __future__ import annotations

import re

import pdfplumber

from application.ports.document_parser_port import DocumentParserPort


class PdfParserAdapter(DocumentParserPort):
    """pdfplumber-based PDF parser adapter."""

    def parse(self, path: str) -> str:
        full_text = ""

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        return clean_text(full_text)


def clean_text(text: str) -> str:
    """
    Lightweight cleaning for LLM consumption.

    Key choice: preserve line breaks to keep "LABEL: value" proximity intact for forms.
    """
    # Normalize Windows line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse runs of spaces/tabs, but keep newlines
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # fix spacing before punctuation
    text = text.replace(" :", ":")
    text = text.replace(" ,", ",")

    return text.strip()
