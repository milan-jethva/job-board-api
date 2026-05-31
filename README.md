# job-board-api
Production-ready Job Board REST API built with FastAPI, PostgreSQL, JWT Auth, Docker

## Quick Start

1. Clone the repo
   git clone https://github.com/milan-jethva/job-board-api.git
   cd job-board-api

2. Create .env file
   copy .env.example .env
   # Fill in your credentials in .env

3. Run with Docker
   docker compose up --build -d
   docker compose exec api alembic upgrade head

4. Visit http://localhost:8000/docs

