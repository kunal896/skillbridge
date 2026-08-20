# Setup

## Environment file

`.env.example` is a safe template of the environment variables the project
expects.

To work locally:

    copy .env.example .env

Then put your actual secret/API values into `.env`.

`.env` is ignored by Git and must never be committed.

## Database

Once Docker is installed:

    docker compose up -d postgres

The local database URL is:

    postgresql://skillbridge:skillbridge@localhost:5432/skillbridge

## Development order

1. Shared contracts
2. Backend skeleton
3. Frontend skeleton
4. RAG ingestion and retrieval
5. Diagnosis agent
6. Roadmap agent
7. Verification
8. Matching
9. Integration
10. Deployment
