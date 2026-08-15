from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "job-market-retrieval"
    app_env: str = "development"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "jobs"

    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    default_top_k: int = 10
    max_top_k: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
