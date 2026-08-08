# Deployment & DevOps Guide

## Architecture Overview
The IPL Analytics platform is containerized using Docker, allowing seamless portability across any operating system.

It is composed of two primary services orchestrated by `docker-compose`:
1. **postgres**: A PostgreSQL 15 database loaded automatically with `sql/ddl/schema.sql` on startup.
2. **streamlit_app**: The Python 3.12 environment running our analytics engine and predictive models.

## Local Deployment Instructions

### Prerequisites
- Docker & Docker Compose installed.
- `.env` file present in the root directory (copy `.env.example`).

### Launching the Stack
1. Start the services:
   ```bash
   docker-compose up -d --build
   ```
2. Verify the containers are healthy:
   ```bash
   docker ps
   ```
3. Access the Streamlit Dashboard:
   - URL: `http://localhost:8501`
4. Access the PostgreSQL Database:
   - Host: `localhost`
   - Port: `5432`

## Continuous Integration (CI)
A GitHub Actions workflow (`.github/workflows/tests.yml`) is triggered on every push and pull request to the `main` branch. 

### CI Pipeline Steps:
1. **Checkout & Setup**: Fetches the code and provisions a clean Python 3.12 environment.
2. **Dependencies**: Installs `requirements.txt` and caches them for faster subsequent builds.
3. **Linting**: Runs `flake8` to enforce PEP-8 compliance and catch critical syntax errors.
4. **Validation**: Verifies the existence of critical structural directories (`models/`, `data/`, etc.).
5. **Testing**: Executes the comprehensive `pytest` suite developed in Phase 11, validating data, DB, transformations, and ML algorithms.

## Security Practices
- **No Hardcoded Credentials**: The `docker-compose.yml` utilizes environment variable substitution. 
- **GitHub Secrets**: CI pipelines that eventually deploy to production must map staging/production DB credentials using `\${{ secrets.DB_PASSWORD }}`. Never expose secrets in plaintext YAML.
