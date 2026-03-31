# Backend Developer Technical Assessment: Data Pipeline

A containerized data pipeline consisting of three services that mock, ingest, and serve customer data. 

## 🏗 Architecture

The system is built using three Docker containers:

1. **Flask Mock Server (`mock-server`):** A REST API running on port `5000`. It serves paginated customer data loaded from a local `customers.json` file.

2. **FastAPI Pipeline (`pipeline-service`):** The core ingestion and serving API running on port `8000`. It exposes an endpoint to trigger data ingestion from the Flask server into the database using the `dlt` (Data Load Tool) library, handling pagination and upserts automatically. It also exposes endpoints to query the ingested data.

3. **PostgreSQL Database (`postgres`):** The persistent storage layer for the ingested customer data, running on port `5432`.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your machine:
* [Docker Desktop](https://www.docker.com/products/docker-desktop) (running)
* Docker Compose (`docker-compose --version`)
* Git
* Python 3.10+ (for local development/testing)

## 📁 Project Structure

```text
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/
│   │   └── customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── models/
    │   └── customer.py
    ├── services/
    │   └── ingestion.py
    ├── database.py
    ├── Dockerfile
    └── requirements.txt

🚀 Setup & Installation
Clone the repository (if applicable) and navigate to the project root directory.

Start the services using Docker Compose. The --build flag ensures the latest code is packaged into the containers.

Bash
docker-compose up -d --build

Verify containers are running:

Bash
docker-compose ps
You should see postgres, mock-server, and pipeline-service in the "Up" state.

🧪 Testing the Pipeline
You can test the entire flow using curl commands.

1. Test the Flask Mock Server
Verify that the mock server is correctly parsing the JSON file and handling pagination.

Bash
curl "http://localhost:5000/api/customers?page=1&limit=5"

2. Trigger Data Ingestion
Hit the FastAPI ingestion endpoint. This triggers the dlt pipeline to fetch all paginated pages from the Flask API and upsert them into the PostgreSQL database.

Bash
curl -X POST http://localhost:8000/api/ingest
Expected Response: {"status": "success", "records_processed": 20}

3. Retrieve Ingested Data
Query the FastAPI service to retrieve the data from the PostgreSQL database.

Get paginated customers:

Bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
Get a single customer by ID:
(Replace CUST-001 with a valid ID from your dataset)

Bash
curl http://localhost:8000/api/customers/CUST-001
🛠 Design Decisions & Notes
Data Ingestion Tool (dlt): Used to streamline the ETL process. dlt natively handles fetching the generator data, inferring the schema, and executing the MERGE (upsert) operation on the PostgreSQL database without writing complex SQL statements.

Schema Management: SQLAlchemy is used for querying the database (models/customer.py), but Base.metadata.create_all is intentionally omitted. dlt acts as the source of truth for table creation during the initial ingestion run, preventing strict SQL type conflicts when moving data from JSON strings to database columns.

Error Handling: The ingestion pipeline includes load_info.raise_on_failed_jobs() to prevent silent failures during the ETL process, ensuring data integrity. The API endpoints include try/except blocks to handle queries made before the database table is initialized by the ingestion process.

🧹 Cleanup
To stop the containers and remove the volumes (which will wipe the database data):

Bash
docker-compose down -v
