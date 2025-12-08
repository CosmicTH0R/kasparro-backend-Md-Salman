Kasparro Backend Assignment

Overview

This is a production-grade backend system designed for high-performance ETL (Extract, Transform, Load) operations. It ingests cryptocurrency data from multiple sources, normalizes it into a unified schema, and exposes it via a RESTful API.

The system is fully containerized using Docker, follows a clean architecture pattern, and is deployed on the cloud with automated scheduling.

🚀 Features Implemented

P0: Foundation Layer (Complete)
  -> Multi-Source Ingestion:
      CoinPaprika API: Fetches live crypto market data.
      CSV Source: Parses legacy local data archives.

  -> Unified Schema: All data is normalized into a single unified_data PostgreSQL table.

  -> Data Validation: Strict type checking and cleaning using Pydantic.

  -> API Service: Fast, paginated access to data via GET /data.

  -> Dockerized: Fully runnable via make up and docker-compose.

P1: Growth Layer (Complete)

  -> Third Data Source: CoinGecko API added for broader market coverage.

  -> Idempotency: Implemented data hashing to prevent duplicate records during ingestion.

  -> Observability: GET /stats endpoint provides real-time ETL job metrics (status, records processed, timestamps).

  -> Robustness: Automatic retry logic for database connections to prevent race conditions.

P2: Differentiator Layer (Bonus)

  -> Cloud Scheduling: Integrated APScheduler to run the ETL pipeline automatically every hour in the background.

  -> Clean Architecture: Modular code structure separating ingestion, api, and core logic for scalability.

🛠 Tech Stack

-> Language: Python 3.9

-> Framework: FastAPI

-> Database: PostgreSQL 15

-> ORM: SQLAlchemy

-> Validation: Pydantic

-> Scheduling: APScheduler

-> Containerization: Docker & Docker Compose

-> Deployment: Render

🏗 Project Structure

The project follows a modular "Clean Architecture" layout to separate concerns:
kasparro-backend/
├── src/
│   ├── api/            # API Routes & Controllers
│   ├── core/           # Database Config & Models
│   ├── ingestion/      # ETL Logic (Extractors & Transformers)
│   ├── schemas/        # Pydantic Validation Models
│   └── main.py         # App Entry Point & Scheduler
├── tests/              # Unit & Integration Tests
├── Dockerfile          # Docker Image Configuration
├── docker-compose.yml  # Multi-container Setup (App + DB)
├── Makefile            # Shortcut Commands
├── requirements.txt    # Python Dependencies
└── README.md           # Documentation

🏃‍♂️ How to Run Locally
Prerequisites
-> Docker & Docker Compose installed.

Steps :

1.Clone the repository:
git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/kasparro-backend-firstname-lastname.git
cd kasparro-backend-firstname-lastname

2.Start the System:
make up
# OR if you don't have 'make' installed:
docker-compose up --build -d

3.Access the API:
Data Endpoint: http://localhost:8000/data
Stats Endpoint: http://localhost:8000/stats
API Documentation: http://localhost:8000/docs

4.Run Manual ETL (Optional):
The ETL runs automatically on startup. To force a run manually:
docker-compose exec app python -m src.ingestion.pipeline

5.Stop the System:
make down

☁️ Cloud Deployment

The system is deployed and live on Render.
->Live API URL: [PASTE_YOUR_RENDER_URL_HERE]/data
->Live Stats: [PASTE_YOUR_RENDER_URL_HERE]/stats

Automated Scheduling:
The system uses APScheduler (BackgroundScheduler) running inside the application container to trigger the ETL pipeline every 1 hour automatically. This ensures the database is always up-to-date without external cron dependencies.

🧪 Testing
The project includes a test suite to verify ETL logic and API endpoints.
To run tests:
make test
# OR
docker-compose run app pytest

📝 API Endpoints
GET /health Returns DB connection status.

GET /data Returns paginated, unified data. Supports ?limit=10 page=1

GET /stats Returns metrics about the last ETL run (P1 Requirement).

GET /tables Debug endpoint to list database tables.