"""
Git repository state analysis service
"""

import os
import git
from typing import List, Optional, Dict
from ..models.git_models import (
    GitRepositoryState, FileStatus, Remote, Commit, 
    WorkflowType, GitDiff
)


class GitStateAnalyzer:
    """Analyzes Git repository state and provides context"""
    
    def __init__(self, repo_path: str = "."):
        """Initialize with repository path"""
        self.repo_path = repo_path
        self._repo = None
        
    @property
    def repo(self) -> git.Repo:
        """Get Git repository object"""
        if self._repo is None:
            try:
                self._repo = git.Repo(self.repo_path)
            except git.InvalidGitRepositoryError:
                raise ValueError(f"Not a valid Git repository: {self.repo_path}")
        return self._repo
    
    def get_current_state(self) -> GitRepositoryState:
        """Get current repository state"""
        try:
            # Get current branch
            current_branch = self.repo.active_branch.name
        except TypeError:
            # Detached HEAD state
            current_branch = "HEAD (detached)"
        
        # Get file statuses
        staged_files = self._get_staged_files()
        unstaged_files = self._get_unstaged_files()
        untracked_files = self._get_untracked_files()
        
        # Get remotes
        remotes = self._get_remotes()
        
        # Get recent commits
        recent_commits = self._get_recent_commits(limit=10)
        
        # Check for conflicts
        conflicted_files = self._get_conflicted_files()
        
        # Check if repository is clean
        is_clean = len(staged_files) == 0 and len(unstaged_files) == 0 and len(untracked_files) == 0
        
        # Get ahead/behind info
        ahead_behind = self._get_ahead_behind_info()
        
        return GitRepositoryState(
            current_branch=current_branch,
            staged_files=staged_files,
            unstaged_files=unstaged_files,
            untracked_files=untracked_files,
            remotes=remotes,
            recent_commits=recent_commits,
            conflicted_files=conflicted_files,
            is_clean=is_clean,
            ahead_behind=ahead_behind
        )
    
    def _get_staged_files(self) -> List[FileStatus]:
        """Get staged files"""
        staged_files = []
        
        # Get staged changes
        staged_diff = self.repo.index.diff("HEAD")
        for diff_item in staged_diff:
            status = "modified"
            if diff_item.new_file:
                status = "added"
            elif diff_item.deleted_file:
                status = "deleted"
            elif diff_item.renamed_file:
                status = "renamed"
            
            staged_files.append(FileStatus(
                path=diff_item.a_path or diff_item.b_path,
                status=status
            ))
        
        return staged_files
    
    def _get_unstaged_files(self) -> List[FileStatus]:
        """Get unstaged files"""
        unstaged_files = []
        
        # Get unstaged changes
        unstaged_diff = self.repo.index.diff(None)
        for diff_item in unstaged_diff:
            status = "modified"
            if diff_item.deleted_file:
                status = "deleted"
            
            unstaged_files.append(FileStatus(
                path=diff_item.a_path,
                status=status
            ))
        
        return unstaged_files
    
    def _get_untracked_files(self) -> List[str]:
        """Get untracked files"""
        return list(self.repo.untracked_files)
    
    def _get_remotes(self) -> List[Remote]:
        """Get repository remotes"""
        remotes = []
        for remote in self.repo.remotes:
            remotes.append(Remote(
                name=remote.name,
                url=remote.url,
                fetch_url=remote.url
            ))
        return remotes
    
    def _get_recent_commits(self, limit: int = 10) -> List[Commit]:
        """Get recent commits"""
        commits = []
        try:
            for commit in self.repo.iter_commits(max_count=limit):
                commits.append(Commit(
                    hash=commit.hexsha[:8],
                    message=commit.message.strip(),
                    author=str(commit.author),
                    date=commit.committed_datetime.isoformat(),
                    files_changed=[item.a_path or item.b_path for item in commit.diff(commit.parents[0] if commit.parents else None)]
                ))
        except Exception:
            # Handle case where there are no commits
            pass
        
        return commits
    
    def _get_conflicted_files(self) -> Optional[List[str]]:
        """Get files with merge conflicts"""
        try:
            # Check if we're in a merge state
            merge_head_path = os.path.join(self.repo.git_dir, "MERGE_HEAD")
            if not os.path.exists(merge_head_path):
                return None
            
            # Get conflicted files
            conflicted = []
            for item in self.repo.index.entries:
                if len(self.repo.index.entries[item]) > 1:  # Multiple stages indicate conflict
                    conflicted.append(item[0])
            
            return conflicted if conflicted else None
        except Exception:
            return None
    
    def _get_ahead_behind_info(self) -> Optional[Dict[str, int]]:
        """Get ahead/behind information relative to upstream"""
        try:
            if not self.repo.active_branch.tracking_branch():
                return None
            
            ahead = list(self.repo.iter_commits(
                f"{self.repo.active_branch.tracking_branch()}..{self.repo.active_branch}"
            ))
            behind = list(self.repo.iter_commits(
                f"{self.repo.active_branch}..{self.repo.active_branch.tracking_branch()}"
            ))
            
            return {
                "ahead": len(ahead),
                "behind": len(behind)
            }
        except Exception:
            return None
    
    def detect_workflow(self) -> WorkflowType:
        """Detect the Git workflow being used"""
        branches = [branch.name for branch in self.repo.branches]
        
        # Check for GitFlow pattern
        if any(branch.startswith(('feature/', 'hotfix/', 'release/')) for branch in branches):
            if 'develop' in branches:
                return WorkflowType.GIT_FLOW
        
        # Check for GitHub Flow pattern (feature branches to main)
        if 'main' in branches or 'master' in branches:
            feature_branches = [b for b in branches if '/' in b or b.startswith('feature')]
            if feature_branches:
                return WorkflowType.GITHUB_FLOW
        
        # Check for GitLab Flow pattern
        if any(branch in ['production', 'staging'] for branch in branches):
            return WorkflowType.GITLAB_FLOW
        
        return WorkflowType.CUSTOM
    
    def analyze_diff(self, commit_range: Optional[str] = None) -> GitDiff:
        """Analyze diff for commit range or working directory"""
        if commit_range:
            # Analyze specific commit range
            diff = self.repo.git.diff(commit_range, numstat=True)
        else:
            # Analyze working directory changes
            diff = self.repo.git.diff("HEAD", numstat=True)
        
        files = []
        total_insertions = 0
        total_deletions = 0
        
        if diff:
            for line in diff.split('\n'):
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        insertions = int(parts[0]) if parts[0] != '-' else 0
                        deletions = int(parts[1]) if parts[1] != '-' else 0
                        filepath = parts[2]
                        
                        files.append(FileStatus(
                            path=filepath,
                            status="modified",
                            insertions=insertions,
                            deletions=deletions,
                            changes=insertions + deletions
                        ))
                        
                        total_insertions += insertions
                        total_deletions += deletions
        
        # Generate summary
        file_count = len(files)
        if file_count == 0:
            summary = "No changes detected"
        elif file_count == 1:
            summary = f"1 file changed, {total_insertions} insertions(+), {total_deletions} deletions(-)"
        else:
            summary = f"{file_count} files changed, {total_insertions} insertions(+), {total_deletions} deletions(-)"
        
        return GitDiff(
            files=files,
            total_insertions=total_insertions,
            total_deletions=total_deletions,
            summary=summary,
            is_merge=self._is_merge_in_progress()
        )
    
    def _is_merge_in_progress(self) -> bool:
        """Check if a merge is in progress"""
        merge_head_path = os.path.join(self.repo.git_dir, "MERGE_HEAD")
        return os.path.exists(merge_head_path)
    
    def get_branch_info(self, branch_name: Optional[str] = None) -> Dict:
        """Get detailed information about a branch"""
        if branch_name is None:
            branch = self.repo.active_branch
        else:
            branch = self.repo.branches[branch_name]
        
        info = {
            "name": branch.name,
            "commit": branch.commit.hexsha[:8],
            "message": branch.commit.message.strip(),
            "author": str(branch.commit.author),
            "date": branch.commit.committed_datetime.isoformat()
        }
        
        # Add tracking info if available
        if hasattr(branch, 'tracking_branch') and branch.tracking_branch():
            info["tracking"] = branch.tracking_branch().name
        
        return info