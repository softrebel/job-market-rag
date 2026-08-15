# Job Market RAG

A comprehensive Retrieval-Augmented Generation (RAG) system for analyzing the job market in Iran. This project crawls, processes, indexes, and retrieves job postings to provide intelligent insights and data-driven analysis of the job market in Iran.

## Architecture

The system follows a scalable microservices architecture, divided into three core components:

1. **[Ingestion Service](./ingestion)**
   - **Role:** Crawls, extracts, cleans, and deduplicates job postings from various external sources (e.g., Jobinja).
   - **Mechanism:** Uses Redis for deduplication and publishes unique job postings to Redis Streams (`jobs.ingested`) to notify downstream consumers. Persists raw and processed data in PostgreSQL.
   - **Key Tech:** Celery, Redis, PostgreSQL, SQLAlchemy, BeautifulSoup4.

2. **[Indexing Service](./indexing)**
   - **Role:** Consumes the clean job postings from the ingestion stream and prepares them for semantic search.
   - **Mechanism:** Generates vector embeddings for job descriptions and metadata using machine learning models, then indexes them in a vector database for fast similarity search.
   - **Key Tech:** Qdrant, Sentence Transformers, Scikit-learn, Redis, Pydantic.

3. **[Retrieval Service](./retrieval)**
   - **Role:** Acts as the query interface for the RAG system.
   - **Mechanism:** Provides a high-performance REST API that takes user queries, converts them into embeddings, and performs vector similarity searches against the indexed job market data to retrieve the most relevant postings.
   - **Key Tech:** FastAPI, Uvicorn, Qdrant Client, Sentence Transformers.

## Technologies Used

- **Language:** Python >= 3.12
- **Data Processing & Queue:** Celery, Redis Streams
- **Databases:** PostgreSQL (Relational Data), Redis (Caching & Deduplication)
- **Vector Search Engine:** Qdrant
- **Machine Learning / NLP:** `sentence-transformers`, `scikit-learn`
- **API Framework:** FastAPI
- **Web Scraping:** BeautifulSoup4, lxml
- **Dependency Management:** `uv`

## Getting Started

Each microservice is self-contained with its own dependencies and configuration. Please refer to the specific `README.md` files in each service directory for detailed setup instructions:

- [Ingestion Service Documentation](./ingestion/README.md)
- [Indexing Service Documentation](./indexing/README.md)
- [Retrieval Service Documentation](./retrieval/README.md)

### General Prerequisites

To run the full stack locally, ensure you have the following installed:
- Docker and Docker Compose (for running Redis, PostgreSQL, and Qdrant)
- Python 3.12+
- `uv` package manager (recommended) or `pip`

## System Flow

1. **Scraping:** The `ingestion` service runs Celery workers to crawl job boards.
2. **Processing:** Scraped jobs are normalized, hashed, and checked against Redis for duplicates.
3. **Streaming:** Unique jobs are pushed to a Redis Stream.
4. **Embedding:** The `indexing` service listens to the stream, generates embeddings using `sentence-transformers`, and stores them in Qdrant.
5. **Querying:** A user queries the `retrieval` FastAPI application, which searches Qdrant for semantically similar job postings and returns the results.
