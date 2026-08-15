from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    REDIS_URL: str
    REDIS_STREAM_NAME: str = "jobs.ingested"
    REDIS_CONSUMER_GROUP: str = "job-indexers"
    REDIS_CONSUMER_NAME: str = "indexer-01"

    QDRANT_URL: str = "http://localhost:6333"

    QDRANT_API_KEY: str | None = None

    QDRANT_COLLECTION_NAME: str = "jobs"

    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    EMBEDDING_DEVICE: str = "cpu"
    EMBEDDING_BATCH_SIZE: int = 32

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150

    INDEXING_BATCH_SIZE: int = 32


settings = Settings()
