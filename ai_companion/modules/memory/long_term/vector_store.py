from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
import time
import os


class QdrantVectorStore:
    def __init__(self):
        self.enabled = True

        try:
            self.client = QdrantClient(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY"),
                timeout=2
            )

            self.collection_name = "memory"
            embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            self.embedding_model = embedding_model

            # Create collection if not exists
            existing = self.client.get_collections().collections
            if self.collection_name not in [c.name for c in existing]:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=384,
                        distance=Distance.COSINE
                    ),
                )

            print("✅ Qdrant connected")

        except Exception as e:
            print("❌ Qdrant failed:", e)
            self.enabled = False

    # ✅ ADD MEMORY
    def add(self, user_id: str, text: str, score: int):
        if not self.enabled:
            return

        try:
            vector = self.embedding_model.encode(text).tolist()

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={
                            "text": text,
                            "user_id": user_id,
                            "score": score,
                            "created_at": int(time.time())
                        }
                    )
                ]
            )

        except Exception as e:
            print("Vector add error:", e)

    # ✅ SEARCH MEMORY
    def search(self, user_id: str, query: str, limit: int = 5):
        if not self.enabled:
            return []

        try:
            query_vector = self.embedding_model.encode(query).tolist()

            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter={
                    "must": [
                        {
                            "key": "user_id",
                            "match": {"value": user_id}
                        }
                    ]
                }
            )

            now = time.time()

            def decay_score(r):
                score = r.payload.get("score", 5)
                created = r.payload.get("created_at", now)
                age_hours = (now - created) / 3600
                return score - (age_hours * 0.1)

            ranked = sorted(results, key=decay_score, reverse=True)

            return [
                r.payload for r in ranked
                if decay_score(r) > 3
            ]

        except Exception as e:
            print("Vector search error:", e)
            return []