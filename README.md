# Dockerized Python App with CI/CD Pipeline

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.0-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker Hub](https://img.shields.io/badge/Registry-Docker%20Hub-0db7ed?logo=docker&logoColor=white)](https://hub.docker.com/)

A containerized Python Flask web microservice powered by an automated GitHub Actions CI/CD pipeline. On every commit, the pipeline lints the code, executes automated unit tests, builds a lightweight non-root production Docker image, performs a container smoke check, and automatically publishes the versioned image to Docker Hub.

---

## Architecture & CI/CD Pipeline Flow

```
  +-------------------------------------------------------------------------+
  |                     Developer Git Push / Pull Request                   |
  +-------------------------------------------------------------------------+
                                     │
                                     ▼
  +-------------------------------------------------------------------------+
  |                    GitHub Actions Workflow: ci-cd.yml                   |
  +-------------------------------------------------------------------------+
       │
       ├──> [Job 1: Code Quality & Unit Tests]
       │       ├── Checkout Source Code
       │       ├── Setup Python 3.11 Runtime
       │       ├── Install Dependencies & Dev Tools
       │       ├── Flake8 Syntax & Code Style Linting
       │       └── Pytest Unit & Integration Tests (/health, /api/info)
       │
       └──> [Job 2: Build, Verify & Publish] (Triggered on push to main)
               ├── Setup QEMU & Docker Buildx
               ├── Authenticate with Docker Hub (Secrets)
               ├── Build Optimized Container Image (Python 3.11-slim)
               ├── Execute Smoke Health Check (curl http://localhost:5000/health)
               └── Publish Tagged Images to Docker Hub:
                     • <username>/flask-cicd-app:latest
                     • <username>/flask-cicd-app:sha-<commit>
```

---

## Features

- **Microservice Application**: Clean Python Flask app providing interactive dashboard, `/health` endpoint for orchestrator probes, and `/api/info` metadata.
- **Production-Hardened Dockerfile**:
  - Based on official `python:3.11-slim` for minimal attack surface.
  - Runs under an unprivileged user (`appuser` UID 1001) instead of root.
  - Native Docker `HEALTHCHECK` directive.
  - High-performance WSGI serving via `gunicorn`.
- **Comprehensive CI/CD Automation**:
  - Pre-merge validation on PRs and automated publishing on merge to `main`.
  - Layer caching using GitHub Actions cache (`type=gha`) for ultra-fast build speeds.
  - Automated smoke test verifying image runtime health prior to publishing.

---

## Repository Structure

```
docker-flask-cicd-pipeline/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD pipeline definition
├── app/
│   ├── templates/
│   │   └── index.html         # Responsive web dashboard
│   ├── __init__.py
│   └── main.py                # Core Flask application & endpoints
├── tests/
│   └── test_app.py            # Automated unit tests (pytest)
├── .dockerignore              # Prevents unnecessary files in Docker context
├── .gitignore                 # Python & environment git exclusions
├── docker-compose.yml         # Local container orchestration file
├── Dockerfile                 # Multi-stage / hardened container specification
├── requirements.txt           # Production dependencies (Flask, Gunicorn)
├── requirements-dev.txt       # Testing dependencies (Pytest, Flake8)
└── README.md                  # Project documentation
```

---

## Getting Started Locally

### 1. Run with Python Virtual Environment

```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd docker-flask-cicd-pipeline

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run unit tests
pytest -v tests/

# Start development server
python app/main.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

### 2. Run with Docker Locally

Build and run using Docker:
```bash
# Build the Docker image
docker build -t flask-cicd-app:local .

# Run the container
docker run -d -p 5000:5000 --name flask_app flask-cicd-app:local

# Verify running container
docker ps
curl http://localhost:5000/health
```

Or run via Docker Compose:
```bash
docker compose up -d
docker compose logs -f
docker compose down
```

---

## Setting up GitHub Actions & Docker Hub

To enable automated publishing from your GitHub repository to Docker Hub:

### Step 1: Create a Docker Hub Access Token
1. Log in to [Docker Hub](https://hub.docker.com/).
2. Navigate to **Account Settings** > **Security** > **New Access Token**.
3. Description: `github-actions-ci-cd`. Permissions: `Read & Write`.
4. Copy the generated Access Token.

### Step 2: Configure GitHub Repository Secrets
1. In your GitHub repository, navigate to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** and add the following two secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username.
   - `DOCKERHUB_TOKEN`: The Personal Access Token generated in Step 1.

### Step 3: Trigger the Pipeline
Push a commit to the `main` branch:
```bash
git add .
git commit -m "feat: trigger automated CI/CD build"
git push origin main
```
Navigate to the **Actions** tab in GitHub to watch the workflow execute linting, tests, build, and push in real-time.

---

## API Endpoints Reference

| Endpoint | Method | Description | Sample Response |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Web Dashboard | HTML Interface |
| `/health` | `GET` | Container Health Check | `{"status":"healthy","version":"1.0.0"}` |
| `/api/info` | `GET` | App and System Metadata | `{"app_name":"Dockerized Flask CI/CD Demo", ...}` |
