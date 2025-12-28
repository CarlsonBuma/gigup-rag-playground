import ollama
from .config import Config

class OllamaClient:
    def __init__(self):
        self.client = ollama.Client(host=Config.OLLAMA_URL)
        self.model = Config.OLLAMA_MODEL

    def generate(self, prompt: str):
        try:
            response = self.client.generate(model=self.model, prompt=prompt)
            return response.get("response", "")
        except Exception as e:
            return f"[Ollama Error] {str(e)}"

    def embed(self, text: str):
        try:
            response = self.client.embeddings(model=self.model, prompt=text)
            return response.get("embedding")
        except Exception as e:
            print("[Embedding Error]", e)
            return None
