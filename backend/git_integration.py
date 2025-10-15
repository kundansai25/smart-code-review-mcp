# Simple Git operations and GitHub PR creator using PyGithub & GitPython
from git import Repo
from github import Github
import os, json, tempfile, uuid, pathlib, shutil

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # set as env var

class GitIntegrator:
    def clone_to(self, repo_url: str, branch: str, dst: str):
        repo = Repo.clone_from(repo_url, dst, branch=branch)
        return repo

    def collect_files(self, repo_root: str, paths=None):
        # Return list of relative file paths to analyze
        out = []
        for root, dirs, files in os.walk(repo_root):
            # skip .git
            if ".git" in root.split(os.sep):
                continue
            for f in files:
                if f.endswith(('.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c', '.jsx', '.tsx')):
                    rel = os.path.relpath(os.path.join(root, f), repo_root)
                    out.append(rel)
        # Optionally filter by given paths
        if paths:
            out = [p for p in out if any(p.startswith(q) for q in paths)]
        return sorted(out)

    def create_pr_with_patches(self, repo_root: str, reports, base_branch="main"):
        token = GITHUB_TOKEN
        if not token:
            print("GITHUB_TOKEN not set; skipping PR creation.")
            return None
        gh = Github(token)
        # expects to find a remote 'origin' with an https URL
        repo = Repo(repo_root)
        origin_url = next(repo.remote().urls)
        # derive owner/repo
        # support both github.com/owner/repo.git and git@github.com:owner/repo.git
        if origin_url.startswith("git@"):
            path = origin_url.split(":",1)[1]
        else:
            path = origin_url.split("github.com/",1)[1]
        path = path.rstrip(".git")
        owner, name = path.split("/",1)
        ghrepo = gh.get_repo(f"{owner}/{name}")
        # Create branch
        new_branch = f"automated/codefixes-{uuid.uuid4().hex[:6]}"
        repo.git.checkout("-b", new_branch)
        # Apply patches (reports contain 'path' and 'suggested_patch' as unified diff or new content)
        for r in reports:
            target = os.path.join(repo_root, r['path'])
            with open(target, "w", encoding="utf-8") as fh:
                fh.write(r['suggested_content'])
            repo.index.add([r['path']])
        repo.index.commit("Automated fixes suggested by Smart Code Review MCP")
        # Push branch
        repo.remote().push(new_branch)
        # Create PR
        pr = ghrepo.create_pull(title="Automated fixes from Smart Code Review MCP",
                                body="This PR contains automated suggestions created by the MCP assistant.",
                                head=new_branch, base=base_branch)
        return pr.html_url
