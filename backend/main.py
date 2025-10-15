from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.mcp import MCPCoordinator
import os

app = FastAPI(title="Smart Code Review MCP")

# Coordinator instance (singleton for simplicity)
coordinator = MCPCoordinator()

class ReviewRequest(BaseModel):
    repo_url: str
    branch: str = "main"
    paths: list[str] | None = None
    max_changes: int = 5

@app.post("/mcp/review")
async def request_review(payload: ReviewRequest):
    try:
        task = await coordinator.start_review(
            repo_url=payload.repo_url,
            branch=payload.branch,
            paths=payload.paths,
            max_changes=payload.max_changes,
        )
        return {"status": "ok", "task": task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}
