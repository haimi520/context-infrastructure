from typing import List

from openai import OpenAI


class EmbeddingClient:
    def __init__(self, base_url: str = "http://localhost:1234/v1", model: str = "text-embedding-qwen3-embedding-8b"):
        import os
        import sys
        from pathlib import Path
        tools_dir = str(Path(__file__).resolve().parents[2])
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        from secret_helper import get_secret
        api_key = get_secret("SEMANTIC_EMBEDDING_API_KEY") or os.getenv("SEMANTIC_EMBEDDING_API_KEY", "lm-studio")
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def embed(self, text: str) -> List[float]:
        """获取单条文本的 embedding。"""
        text = text.replace("\n", " ")
        try:
            resp = self.client.embeddings.create(input=[text], model=self.model)
            return resp.data[0].embedding
        except Exception as e:
            print(f"Embedding error: {e}")
            raise

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """批量获取 embedding。"""
        results = []
        for i in range(0, len(texts), batch_size):
            batch = [t.replace("\n", " ") for t in texts[i:i+batch_size]]
            try:
                resp = self.client.embeddings.create(input=batch, model=self.model)
                results.extend([d.embedding for d in resp.data])
            except Exception as e:
                print(f"Batch embedding error at index {i}: {e}")
                raise
        return results
