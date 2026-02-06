from __future__ import annotations

from typing import Protocol


class DocumentParserPort(Protocol):
    """Port for parsing documents into raw text."""

    def parse(self, path: str) -> str: ...
