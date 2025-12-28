from pathlib import Path
from typing import List
import pdfplumber


class PDFChunker:
    """
    MVP utility for:
    1. Loading PDF text
    2. Chunking text into manageable pieces
    """

    def load_pdf(self, path: str) -> str:
        """
        Extracts text from a PDF file using pdfplumber.
        Returns a single string.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text.strip()

    def chunk_text(self, text: str, max_chars: int = 800) -> List[str]:
        """
        MVP chunking strategy:
        - Split by paragraphs (double newline)
        - If a paragraph is too long, split into fixed-size chunks
        """
        paragraphs = text.split("\n\n")
        chunks = []

        for p in paragraphs:
            p = p.strip()
            if not p:
                continue

            if len(p) <= max_chars:
                chunks.append(p)
            else:
                # Split long paragraphs into smaller chunks
                for i in range(0, len(p), max_chars):
                    chunks.append(p[i:i + max_chars])

        return chunks

    def process_pdf(self, path: str, max_chars: int = 800) -> List[str]:
        """
        Full pipeline:
        - Load PDF
        - Chunk text
        - Return list of chunk strings
        """
        text = self.load_pdf(path)
        return self.chunk_text(text, max_chars=max_chars)
