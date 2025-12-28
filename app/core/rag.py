from pgvector.psycopg import Vector
from .database import Database
from .ollama_client import OllamaClient
from .pdf_chunker import PDFChunker

class RAG:
    def __init__(self):
        self.db = Database()
        self.llm = OllamaClient()
        self.chunker = PDFChunker()

    def chunk_pdf(self, pdf_path: str):
        chunks = self.chunker.process_pdf(pdf_path)

        doc_id = self.add_document(
            title=pdf_path,
            description="PDF document",
            source_type="pdf"
        )

        for idx, chunk in enumerate(chunks):
            self.add_chunk(doc_id, idx, chunk)

        return chunks

    def add_document(self, title, description=None, source_type=None):
        conn = self.db.connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (title, description, source_type)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (title, description, source_type)
            )
            doc_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return doc_id

    def add_chunk(self, document_id, chunk_index, content):
        embedding = self.llm.embed(content)
        token_count = len(content.split())

        conn = self.db.connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chunks (document_id, chunk_index, content, embedding, token_count)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (document_id, chunk_index, content, embedding, token_count)
            )
        conn.commit()
        conn.close()

    ## Vector similarity search
    def search(self, query, limit=3):
        qvec = Vector(self.llm.embed(query))

        conn = self.db.connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    id,
                    content,
                    embedding <-> %s AS distance
                FROM chunks
                ORDER BY distance DESC
                LIMIT %s
                """,
                (qvec, limit)
            )
            rows = cur.fetchall()
        conn.close()
        return rows

    ## LLM answer
    def answer(self, query):
        results = self.search(query)

        context = "\n".join([row[1] for row in results])

        prompt = f"""
            Context:
            {context}

            Question:
            {query}

            Task:
            Use ONLY the context above.

            Your job:
            1. Answer the question briefly.
            2. Identify which parts of the context are relevant to the question.
            3. Explain briefly why the context matches the question.

            Rules:
            - Do NOT invent information.
            - Do NOT add details not present in the context.
            - Keep explanations short and factual.

            Format:

            Answer:
            <short answer>

            Relevant Evidence:
            - "<exact phrase or sentence from the context>"

            Why This Fits:
            <1–2 short sentences>
        """

        return self.llm.generate(prompt)



