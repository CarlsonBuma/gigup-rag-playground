class Chunk:
    def __init__(self, id, document_id, chunk_index, content, embedding, token_count):
        self.id = id
        self.document_id = document_id
        self.chunk_index = chunk_index
        self.content = content
        self.embedding = embedding
        self.token_count = token_count
