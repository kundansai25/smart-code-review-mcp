# Smart Code Review & Bug Fix Assistant (MCP)

An end-to-end reference implementation of a **Smart Code Review & Bug Fix Assistant** that follows a Model Context Protocol (MCP) pattern, using Retrieval-Augmented Generation (RAG), Git integration, and tooling to analyze repositories and propose fixes.

## Features
- FastAPI backend exposing MCP-style endpoints
- RAG retriever (placeholder) using local chunking + embeddings (abstracted)
- Code analysis and fix suggestion workflow
- GitHub integration to fetch code, create branches, and open PRs (uses `PyGithub`)
- Dockerfile and GitHub Actions CI
- Example frontend stub (React) to interact with assistant
- Clear instructions to run locally and push to your own Git repo

> **Note:** This repo contains placeholders for model/embedding APIs. Replace `OPENAI_API_KEY` or other provider keys in environment variables or GitHub Secrets.

## Quickstart (local)
1. Clone this repo (after downloading or creating it).
2. Create and activate a Python virtualenv:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Set environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export GITHUB_TOKEN="ghp_..."
```
4. Run the API:
```bash
uvicorn backend.main:app --reload --port 8000
```
5. Use the frontend (open `frontend/README.md`) or call the `/mcp/review` endpoint.

## How to upload to Git
1. Create a new empty repo on GitHub.
2. In this project folder:
```bash
git init
git add .
git commit -m "Initial commit - Smart Code Review MCP reference"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```
Set GitHub Actions secrets `OPENAI_API_KEY` and `GITHUB_TOKEN` in repo settings.

## Project Layout
- `backend/` - FastAPI service + core logic
- `frontend/` - React stub (single-file demo)
- `.github/workflows/` - CI workflow
- `Dockerfile`, `docker-compose.yml`, `requirements.txt` - deployment & deps

