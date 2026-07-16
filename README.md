# AI Workspace

An AI SaaS platform for knowledge management.

## Features

- Chat
- RAG
- AI Agent
- Workspace
- Authentication
- Dashboard

## Stack

- Next.js
- FastAPI
- PostgreSQL
- Docker
- Qdrant

## Docker

Jalankan development dari root repository:

```powershell
docker compose --env-file .env -f infrastructure/compose/docker-compose.dev.yml up --build
```

Untuk production, gunakan password PostgreSQL yang kuat di `.env`, lalu:

```powershell
docker compose --env-file .env -f infrastructure/compose/docker-compose.prod.yml up --build -d
```

Jika port 3000, 5432, 6333, atau 8000 sudah dipakai, ubah `WEB_PORT`,
`POSTGRES_PORT`, `QDRANT_PORT`, atau `API_PORT` pada `.env` sebelum menjalankan Compose.
