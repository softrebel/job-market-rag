import pytest
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.embeddings.sentence_transformer import SentenceTransformerEmbedder


TEST_COLLECTION = "jobs_test"

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@pytest.fixture
def qdrant_client():
    client = QdrantClient(
        url="http://localhost:6333",
    )

    if client.collection_exists(TEST_COLLECTION):
        client.delete_collection(TEST_COLLECTION)

    embedder = SentenceTransformerEmbedder(
        model_name=EMBEDDING_MODEL,
    )

    vector_size = embedder.dimension

    client.create_collection(
        collection_name=TEST_COLLECTION,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )

    yield client

    if client.collection_exists(TEST_COLLECTION):
        client.delete_collection(TEST_COLLECTION)


@pytest.fixture
def test_data(qdrant_client):
    embedder = SentenceTransformerEmbedder(
        model_name=EMBEDDING_MODEL,
    )

    texts = [
        "Senior Python Django Backend Developer",
        "Frontend Developer React TypeScript",
        "Python Data Engineer PostgreSQL",
    ]

    vectors = embedder.embed(texts)

    points = [
        PointStruct(
            id=1,
            vector=vectors[0],
            payload={
                "job_id": "1",
                "title": "Senior Backend Developer",
                "company": "Sedreh",
                "description": ("Python Django PostgreSQL Backend Developer"),
                "city": "تهران، تهران",
                "source": "jobinja",
                "url": "https://example.com/1",
                "chunk_id": "1_0",
                "skills": [
                    "Python",
                    "Django",
                    "PostgreSQL",
                ],
            },
        ),
        PointStruct(
            id=2,
            vector=vectors[1],
            payload={
                "job_id": "2",
                "title": "Frontend Developer",
                "company": "Example",
                "description": ("React TypeScript Developer"),
                "city": "تهران، تهران",
                "source": "jobinja",
                "url": "https://example.com/2",
                "chunk_id": "2_0",
                "skills": [
                    "React",
                    "TypeScript",
                ],
            },
        ),
        PointStruct(
            id=3,
            vector=vectors[2],
            payload={
                "job_id": "3",
                "title": "Data Engineer",
                "company": "DataCo",
                "description": ("Python Data Engineer with PostgreSQL"),
                "city": "اصفهان، اصفهان",
                "source": "jobinja",
                "url": "https://example.com/3",
                "chunk_id": "3_0",
                "skills": [
                    "Python",
                    "PostgreSQL",
                ],
            },
        ),
    ]

    qdrant_client.upsert(
        collection_name=TEST_COLLECTION,
        points=points,
    )

    return qdrant_client
