from pathlib import Path
from typing import List
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PdfChunker:
    """Extracts and chunks text from PDF files using a modern RAG-friendly splitter."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "! ",
                "? ",
                ", ",
                " ",
                ""
            ],
        )

    def load_pdf(self, path: str) -> str:
        pdf_path = Path(path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        text_parts = []

        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)

            for page in reader.pages:
                page_text = page.extract_text()

                if not page_text:
                    continue

                cleaned = (
                    page_text.replace("\xa0", " ")
                    .replace("\t", " ")
                    .strip()
                )

                if cleaned:
                    text_parts.append(cleaned)

        return "\n\n".join(text_parts).strip()

    def chunk_text(self, text: str) -> List[str]:
        return self.splitter.split_text(text)

    def process_pdf(self, path: str) -> List[str]:
        text = self.load_pdf(path)
        return self.chunk_text(text)
