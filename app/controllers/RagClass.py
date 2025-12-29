from core.database import Database
from core.ollama import Ollama
from core.modules.chunker import Chunker
from .rag.RagRetrievalController import RagRetrievalController
from .rag.RagIngestionController import RagIngestionController

class RagClass:
    def __init__(self):
        self.db = Database()
        self.ollama = Ollama()
        self.chunker = Chunker()
        self.ingest = RagIngestionController(self.db, self.ollama, self.chunker) 
        self.retrieve = RagRetrievalController(self.db, self.ollama)
