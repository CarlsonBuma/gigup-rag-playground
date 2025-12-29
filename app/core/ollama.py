import ollama
from .config import Config


class Ollama:
    def __init__(self):
        self.client = ollama.Client(host=Config.OLLAMA_URL)
        self.llm_model = Config.OLLAMA_LLM_MODEL
        self.embedding_model = Config.OLLAMA_EMBEDDING_MODEL

    # -----------------------------
    # LLM Text Generation
    # -----------------------------
    def generate(self, prompt: str):
        try:
            response = self.client.generate(
                model=self.llm_model,
                prompt=prompt
            )
            return response.get("response", "")
        except Exception as e:
            return f"[Ollama Error] {str(e)}"

    # -----------------------------
    # Embeddings
    # -----------------------------
    def embed(self, text: str):
        try:
            response = self.client.embeddings(
                model=self.embedding_model,
                prompt=text
            )
            return response.get("embedding")
        except Exception as e:
            print("[Embedding Error]", e)
            return None
