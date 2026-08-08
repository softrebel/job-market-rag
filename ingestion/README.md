# Job Market RAG - Ingestion Service

This project is the **Ingestion Service** for the Job Market RAG system. It is responsible for crawling, extracting, processing, and publishing job postings from various sources into the system's data pipeline. 

The service features a robust, extensible pipeline to process job postings, including data normalization, deduplication (using Redis), and streaming (via Redis Streams) to downstream services, with persistence provided by PostgreSQL.

## Architecture & Pipeline

The ingestion process runs jobs through a configurable `IngestionPipeline` containing sequential stages:

1. **Extraction**: Extractors pull raw jobs from external sources (e.g., Jobinja via crawlers) or existing databases.
2. **Normalization Stage**: Cleans and standardizes job data (text cleaning, format adjustments).
3. **Hash Stage**: Generates a unique content hash for each job to detect identical entries.
4. **Deduplicate Stage**: Leverages a Redis-backed store to check and drop already processed jobs.
5. **Publish Stage**: Pushes new unique jobs to Redis Streams (`jobs.ingested`) to notify downstream consumers.

## Tech Stack

- **Python**: `>=3.12`
- **Dependency Management**: `uv` (lockfile provided) or `pip` (via `pyproject.toml`)
- **Database**: PostgreSQL (SQLAlchemy + Alembic)
- **Caching & Messaging**: Redis (Streams)
- **Web Scraping**: BeautifulSoup4, lxml
- **Task Queue**: Celery
- **Configuration**: Pydantic Settings

## Project Structure

- `src/app`: Main entrypoint (`main.py`)
- `src/config`: Environment configurations and logging setup
- `src/database`: Database models, session management, and base classes
- `src/domain`: Domain entities (`CanonicalJob`, `JobMessage`, etc.)
- `src/extractors`: Web crawlers (e.g., Jobinja) and database extractors
- `src/pipeline`: Configurable processing pipeline and stage definitions
- `src/dedup`: Deduplication logic (RedisStore)
- `src/messaging`: Event publishers (RedisStreamPublisher)
- `src/mappers`: Data mapping between raw inputs, domain models, and database records
- `src/repositories`: Database repository patterns
- `src/services`: Shared business logic (hashing, cleaning, CDNs)
- `src/workers`: Celery workers and task definitions

## Setup & Execution

### Prerequisites

Ensure you have Docker, Docker Compose, and Python 3.12+ installed on your machine. 

### 1. Environment Configuration

Copy the example environment file and configure the settings (including Postgres credentials, Redis URL, and Crawler accounts):

```bash
cp .env.example .env
```

*Note: Ensure your `ENABLED_SOURCES` and database parameters are properly set in `.env`.*

### 2. Infrastructure (Redis)

Start the required infrastructure using Docker Compose:

```bash
docker-compose up -d
```

### 3. Install Dependencies

You can install dependencies using either `uv` or `pip`:

**Using `uv` (Recommended):**
```bash
uv venv .venv
# Activate venv depending on your OS (e.g., source .venv/bin/activate)
uv pip install -e .
```

**Using standard `pip`:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### 4. Running the Application

Execute the main pipeline:

```bash
python -m src.app.main
```

## Worker Execution

The ingestion service relies on Celery for asynchronous processing. To start the Celery worker:

```bash
celery -A src.workers.celery worker --loglevel=info
```
