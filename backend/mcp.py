# MCPCoordinator: Orchestrates the steps of the Model Context Protocol:
# 1. Fetch repo
# 2. Chunk & embed code
# 3. Retrieve relevant contexts for problem areas
# 4. Generate suggestions / patches
# 5. Create PR via GitHub (optional)
import asyncio, tempfile, os, shutil
from backend.git_integration import GitIntegrator
from backend.code_analyzer import CodeAnalyzer
from rich import print

class MCPCoordinator:
    def __init__(self):
        self.git = GitIntegrator()
        self.analyzer = CodeAnalyzer()

    async def start_review(self, repo_url: str, branch: str = "main", paths=None, max_changes=5):
        # 1. Clone repo (temp)
        tmpdir = tempfile.mkdtemp(prefix="repo-")
        print(f"[green]Cloning {repo_url} into {tmpdir}[/green]")
        repo = self.git.clone_to(repo_url, branch, tmpdir)
        # 2. Gather files
        file_paths = self.git.collect_files(tmpdir, paths)
        # 3. Analyze and propose fixes (this may include RAG retrieval / LLM calls)
        reports = []
        for i, path in enumerate(file_paths):
            if i >= 200: break
            full = os.path.join(tmpdir, path)
            report = await self.analyzer.analyze_file(full, repo_root=tmpdir)
            if report:
                reports.append(report)
                if len(reports) >= max_changes:
                    break
        # 4. Optionally create branch & PR
        pr_url = None
        if reports:
            pr_url = self.git.create_pr_with_patches(tmpdir, reports, base_branch=branch)
        # Clean up
        shutil.rmtree(tmpdir, ignore_errors=True)
        return {"reports": reports, "pr_url": pr_url}
