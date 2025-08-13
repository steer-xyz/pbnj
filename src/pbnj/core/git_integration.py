"""Git integration helpers for PBNJ."""

import subprocess
from pathlib import Path
from typing import Optional

import git
from git import Repo


class GitHelper:
    """Helper class for Git operations."""
    
    def __init__(self, repo_path: Optional[Path] = None) -> None:
        """Initialize GitHelper with optional repository path."""
        self.repo_path = repo_path or Path.cwd()
        self.repo: Optional[Repo] = None
    
    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository."""
        try:
            git.Repo(self.repo_path)
            return True
        except git.InvalidGitRepositoryError:
            return False
    
    def init_repo(self) -> None:
        """Initialize a new git repository."""
        if self.is_git_repo():
            return
        
        self.repo = Repo.init(self.repo_path)
        
        # Create .gitignore
        gitignore_path = self.repo_path / ".gitignore"
        if not gitignore_path.exists():
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# PBNJ specific
*.pbix
.pbnj/cache/
"""
            gitignore_path.write_text(gitignore_content)
        
        # Initial commit
        self.repo.index.add([".gitignore"])
        self.repo.index.commit("Initial commit - Add .gitignore")
    
    def get_repo(self) -> Repo:
        """Get the git repository object."""
        if self.repo is None:
            self.repo = Repo(self.repo_path)
        return self.repo
    
    def add_files(self, files: list[str]) -> None:
        """Add files to git staging area."""
        repo = self.get_repo()
        repo.index.add(files)
    
    def commit_changes(self, message: str) -> None:
        """Commit all changes with a message."""
        repo = self.get_repo()
        
        # Add all files
        repo.git.add(A=True)
        
        # Check if there are changes to commit
        if not repo.is_dirty():
            return
        
        # Commit changes
        repo.index.commit(message)
    
    def get_status(self) -> dict[str, list[str]]:
        """Get git status information."""
        repo = self.get_repo()
        
        status = {
            "untracked": list(repo.untracked_files),
            "modified": [item.a_path for item in repo.index.diff(None)],
            "staged": [item.a_path for item in repo.index.diff("HEAD")],
        }
        
        return status
    
    def create_branch(self, branch_name: str) -> None:
        """Create and checkout a new branch."""
        repo = self.get_repo()
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()
    
    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        repo = self.get_repo()
        return repo.active_branch.name
    
    def has_remote(self) -> bool:
        """Check if repository has a remote origin."""
        repo = self.get_repo()
        return len(repo.remotes) > 0
    
    def add_remote(self, name: str, url: str) -> None:
        """Add a remote repository."""
        repo = self.get_repo()
        repo.create_remote(name, url)
    
    def push_changes(self, remote: str = "origin", branch: Optional[str] = None) -> None:
        """Push changes to remote repository."""
        repo = self.get_repo()
        
        if branch is None:
            branch = repo.active_branch.name
        
        origin = repo.remote(remote)
        origin.push(branch)