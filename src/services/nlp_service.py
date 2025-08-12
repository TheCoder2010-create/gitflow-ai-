"""
Natural Language Processing service for Git workflow assistance
"""

import re
from typing import List, Dict, Any, Optional
from ..models.git_models import (
    AssistantResponse, GitCommand, RiskLevel, GitRepositoryState, GitDiff
)
from .gpt_service import GPTModelService
from .git_analyzer import GitStateAnalyzer


class NLPService:
    """Natural Language Processing service for Git operations"""
    
    def __init__(self, gpt_service: GPTModelService, git_analyzer: GitStateAnalyzer):
        """Initialize NLP service with GPT and Git analyzer"""
        self.gpt_service = gpt_service
        self.git_analyzer = git_analyzer
        
        # Common Git command patterns
        self.command_patterns = {
            'commit': [
                r'\b(commit|save|record)\b.*\b(changes|files|work)\b',
                r'\bcommit\b',
                r'\bsave.*changes\b'
            ],
            'push': [
                r'\b(push|upload|send)\b.*\b(remote|origin|upstream)\b',
                r'\bpush\b',
                r'\bupload.*changes\b'
            ],
            'pull': [
                r'\b(pull|fetch|download|get|sync)\b.*\b(changes|updates|remote)\b',
                r'\bpull\b',
                r'\bget.*changes\b'
            ],
            'branch': [
                r'\b(create|make|new)\b.*\bbranch\b',
                r'\b(switch|change|checkout)\b.*\bbranch\b',
                r'\bbranch\b'
            ],
            'merge': [
                r'\bmerge\b.*\bbranch\b',
                r'\bmerge\b',
                r'\bcombine.*branches\b'
            ],
            'status': [
                r'\b(status|state|what.*changed)\b',
                r'\bcheck.*status\b',
                r'\bwhat.*files\b'
            ],
            'undo': [
                r'\b(undo|revert|rollback|reset)\b',
                r'\bundo.*commit\b',
                r'\bgo.*back\b'
            ],
            'stash': [
                r'\b(stash|save|store)\b.*\b(changes|work)\b',
                r'\bstash\b',
                r'\btemporary.*save\b'
            ]
        }
    
    def process_user_query(self, query: str, context: Optional[GitRepositoryState] = None) -> AssistantResponse:
        """Process user query and return AI assistant response"""
        # Get current Git context if not provided
        if context is None:
            context = self.git_analyzer.get_current_state()
        
        # Analyze user intent
        intent = self._analyze_intent(query)
        
        # Build context for GPT
        git_context = self._build_git_context(context)
        
        # Generate AI response
        ai_response = self.gpt_service.generate_git_response(query, git_context)
        
        # Parse AI response and generate commands
        suggested_commands = self._generate_commands(intent, query, context, ai_response)
        
        # Generate explanation
        explanation = self._generate_explanation(intent, query, context, ai_response)
        
        # Check for warnings
        warnings = self._check_warnings(suggested_commands, context)
        
        # Generate alternatives if needed
        alternatives = self._generate_alternatives(suggested_commands, context)
        
        return AssistantResponse(
            interpretation=f"I understand you want to {intent['action']} {intent['target']}",
            suggested_commands=suggested_commands,
            explanation=explanation,
            warnings=warnings,
            alternatives=alternatives,
            confidence=intent['confidence']
        )
    
    def _analyze_intent(self, query: str) -> Dict[str, Any]:
        """Analyze user intent from query"""
        query_lower = query.lower()
        
        # Check for command patterns
        for command, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return {
                        'action': command,
                        'target': self._extract_target(query, command),
                        'confidence': 0.8,
                        'raw_query': query
                    }
        
        # Default intent
        return {
            'action': 'help',
            'target': 'general',
            'confidence': 0.5,
            'raw_query': query
        }
    
    def _extract_target(self, query: str, action: str) -> str:
        """Extract target from query based on action"""
        query_lower = query.lower()
        
        if action == 'branch':
            # Extract branch name
            branch_match = re.search(r'branch\s+([a-zA-Z0-9_/-]+)', query_lower)
            if branch_match:
                return branch_match.group(1)
            return 'new branch'
        
        elif action == 'commit':
            # Extract commit message if provided
            msg_match = re.search(r'message\s+["\']([^"\']+)["\']', query)
            if msg_match:
                return msg_match.group(1)
            return 'changes'
        
        elif action == 'merge':
            # Extract branch to merge
            merge_match = re.search(r'merge\s+([a-zA-Z0-9_/-]+)', query_lower)
            if merge_match:
                return merge_match.group(1)
            return 'branch'
        
        return 'repository'
    
    def _build_git_context(self, state: GitRepositoryState) -> Dict[str, Any]:
        """Build Git context for GPT"""
        return {
            'current_branch': state.current_branch,
            'staged_files': [f.path for f in state.staged_files],
            'unstaged_files': [f.path for f in state.unstaged_files],
            'untracked_files': state.untracked_files,
            'is_clean': state.is_clean,
            'has_conflicts': state.conflicted_files is not None,
            'ahead_behind': state.ahead_behind,
            'recent_commits': [c.message for c in state.recent_commits[:3]]
        }
    
    def _generate_commands(self, intent: Dict, query: str, context: GitRepositoryState, ai_response: str) -> List[GitCommand]:
        """Generate Git commands based on intent and context"""
        commands = []
        action = intent['action']
        target = intent['target']
        
        if action == 'commit':
            commands.extend(self._generate_commit_commands(context, target))
        
        elif action == 'push':
            commands.extend(self._generate_push_commands(context))
        
        elif action == 'pull':
            commands.extend(self._generate_pull_commands(context))
        
        elif action == 'branch':
            commands.extend(self._generate_branch_commands(context, target, query))
        
        elif action == 'merge':
            commands.extend(self._generate_merge_commands(context, target))
        
        elif action == 'status':
            commands.extend(self._generate_status_commands(context))
        
        elif action == 'undo':
            commands.extend(self._generate_undo_commands(context, query))
        
        elif action == 'stash':
            commands.extend(self._generate_stash_commands(context))
        
        else:
            # Default help command
            commands.append(GitCommand(
                command="git",
                args=["status"],
                description="Show repository status",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False,
                explanation="Let's start by checking your repository status"
            ))
        
        return commands
    
    def _generate_commit_commands(self, context: GitRepositoryState, target: str) -> List[GitCommand]:
        """Generate commit-related commands"""
        commands = []
        
        # If no files are staged, suggest adding files first
        if not context.staged_files and (context.unstaged_files or context.untracked_files):
            commands.append(GitCommand(
                command="git",
                args=["add", "."],
                description="Stage all changes for commit",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False,
                explanation="First, let's stage your changes"
            ))
        
        # Generate commit command
        if target != 'changes':
            # User provided a commit message
            commands.append(GitCommand(
                command="git",
                args=["commit", "-m", f'"{target}"'],
                description=f"Commit changes with message: {target}",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False
            ))
        else:
            # Generate commit message using AI
            if context.staged_files or context.unstaged_files:
                diff = self.git_analyzer.analyze_diff()
                ai_message = self.gpt_service.generate_commit_message(
                    diff.summary,
                    [f.path for f in diff.files]
                )
                commands.append(GitCommand(
                    command="git",
                    args=["commit", "-m", f'"{ai_message}"'],
                    description=f"Commit with AI-generated message: {ai_message}",
                    risk_level=RiskLevel.SAFE,
                    requires_confirmation=False
                ))
        
        return commands
    
    def _generate_push_commands(self, context: GitRepositoryState) -> List[GitCommand]:
        """Generate push-related commands"""
        commands = []
        
        # Check if there are commits to push
        if context.ahead_behind and context.ahead_behind.get('ahead', 0) > 0:
            commands.append(GitCommand(
                command="git",
                args=["push"],
                description="Push commits to remote repository",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False,
                explanation=f"Push {context.ahead_behind['ahead']} commit(s) to remote"
            ))
        else:
            commands.append(GitCommand(
                command="git",
                args=["push", "-u", "origin", context.current_branch],
                description="Push current branch to remote (first time)",
                risk_level=RiskLevel.MODERATE,
                requires_confirmation=True,
                explanation="This will create the branch on the remote repository"
            ))
        
        return commands
    
    def _generate_pull_commands(self, context: GitRepositoryState) -> List[GitCommand]:
        """Generate pull-related commands"""
        commands = []
        
        # Check if working directory is clean
        if not context.is_clean:
            commands.append(GitCommand(
                command="git",
                args=["stash"],
                description="Stash local changes before pulling",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=True,
                explanation="Stash changes to avoid conflicts during pull"
            ))
        
        commands.append(GitCommand(
            command="git",
            args=["pull"],
            description="Pull latest changes from remote",
            risk_level=RiskLevel.MODERATE,
            requires_confirmation=False,
            explanation="Fetch and merge changes from remote repository"
        ))
        
        return commands
    
    def _generate_branch_commands(self, context: GitRepositoryState, target: str, query: str) -> List[GitCommand]:
        """Generate branch-related commands"""
        commands = []
        query_lower = query.lower()
        
        if 'create' in query_lower or 'new' in query_lower:
            # Create new branch
            branch_name = target if target != 'new branch' else 'feature/new-feature'
            commands.append(GitCommand(
                command="git",
                args=["checkout", "-b", branch_name],
                description=f"Create and switch to new branch: {branch_name}",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False
            ))
        
        elif 'switch' in query_lower or 'checkout' in query_lower:
            # Switch to existing branch
            commands.append(GitCommand(
                command="git",
                args=["checkout", target],
                description=f"Switch to branch: {target}",
                risk_level=RiskLevel.MODERATE,
                requires_confirmation=not context.is_clean,
                explanation="Switching branches with uncommitted changes may lose work"
            ))
        
        else:
            # List branches
            commands.append(GitCommand(
                command="git",
                args=["branch", "-a"],
                description="List all branches",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False
            ))
        
        return commands
    
    def _generate_merge_commands(self, context: GitRepositoryState, target: str) -> List[GitCommand]:
        """Generate merge-related commands"""
        commands = []
        
        # Ensure working directory is clean
        if not context.is_clean:
            commands.append(GitCommand(
                command="git",
                args=["status"],
                description="Check repository status before merge",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False,
                explanation="Clean working directory recommended before merge"
            ))
        
        commands.append(GitCommand(
            command="git",
            args=["merge", target],
            description=f"Merge branch '{target}' into current branch",
            risk_level=RiskLevel.MODERATE,
            requires_confirmation=True,
            explanation="This will combine changes from both branches"
        ))
        
        return commands
    
    def _generate_status_commands(self, context: GitRepositoryState) -> List[GitCommand]:
        """Generate status-related commands"""
        return [
            GitCommand(
                command="git",
                args=["status"],
                description="Show repository status",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False,
                explanation="Display current state of your repository"
            )
        ]
    
    def _generate_undo_commands(self, context: GitRepositoryState, query: str) -> List[GitCommand]:
        """Generate undo-related commands"""
        commands = []
        query_lower = query.lower()
        
        if 'commit' in query_lower:
            if 'keep' in query_lower or 'save' in query_lower:
                # Undo commit but keep changes
                commands.append(GitCommand(
                    command="git",
                    args=["reset", "--soft", "HEAD~1"],
                    description="Undo last commit but keep changes staged",
                    risk_level=RiskLevel.MODERATE,
                    requires_confirmation=True,
                    explanation="This will undo the commit but preserve your changes"
                ))
            else:
                # Undo commit and changes
                commands.append(GitCommand(
                    command="git",
                    args=["reset", "--hard", "HEAD~1"],
                    description="Undo last commit and discard changes",
                    risk_level=RiskLevel.DESTRUCTIVE,
                    requires_confirmation=True,
                    explanation="⚠️ This will permanently delete your changes!"
                ))
        
        else:
            # General undo - show options
            commands.append(GitCommand(
                command="git",
                args=["log", "--oneline", "-5"],
                description="Show recent commits to choose what to undo",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False
            ))
        
        return commands
    
    def _generate_stash_commands(self, context: GitRepositoryState) -> List[GitCommand]:
        """Generate stash-related commands"""
        commands = []
        
        if context.unstaged_files or context.untracked_files:
            commands.append(GitCommand(
                command="git",
                args=["stash", "push", "-m", "Work in progress"],
                description="Stash current changes",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False,
                explanation="Temporarily save your changes"
            ))
        else:
            commands.append(GitCommand(
                command="git",
                args=["stash", "list"],
                description="Show stashed changes",
                risk_level=RiskLevel.SAFE,
                requires_confirmation=False
            ))
        
        return commands
    
    def _generate_explanation(self, intent: Dict, query: str, context: GitRepositoryState, ai_response: str) -> str:
        """Generate explanation for the suggested actions"""
        action = intent['action']
        
        explanations = {
            'commit': f"I'll help you commit your changes. You have {len(context.staged_files)} staged files and {len(context.unstaged_files)} modified files.",
            'push': f"I'll help you push your changes to the remote repository.",
            'pull': f"I'll help you pull the latest changes from the remote repository.",
            'branch': f"I'll help you work with Git branches.",
            'merge': f"I'll help you merge branches safely.",
            'status': f"I'll show you the current status of your repository.",
            'undo': f"I'll help you undo changes safely.",
            'stash': f"I'll help you stash your current work."
        }
        
        base_explanation = explanations.get(action, "I'll help you with that Git operation.")
        
        # Add AI response if it provides additional context
        if ai_response and len(ai_response) > 10:
            return f"{base_explanation} {ai_response}"
        
        return base_explanation
    
    def _check_warnings(self, commands: List[GitCommand], context: GitRepositoryState) -> Optional[List[str]]:
        """Check for potential warnings"""
        warnings = []
        
        # Check for destructive operations
        destructive_commands = [cmd for cmd in commands if cmd.risk_level == RiskLevel.DESTRUCTIVE]
        if destructive_commands:
            warnings.append("⚠️ This operation will permanently delete data. Make sure you have backups.")
        
        # Check for uncommitted changes
        if not context.is_clean:
            push_commands = [cmd for cmd in commands if 'push' in cmd.args]
            if push_commands:
                warnings.append("💡 You have uncommitted changes. Consider committing them first.")
        
        # Check for merge conflicts
        if context.conflicted_files:
            warnings.append("⚠️ You have unresolved merge conflicts. Resolve them before proceeding.")
        
        return warnings if warnings else None
    
    def _generate_alternatives(self, commands: List[GitCommand], context: GitRepositoryState) -> Optional[List[GitCommand]]:
        """Generate alternative commands if applicable"""
        alternatives = []
        
        # For destructive operations, provide safer alternatives
        for cmd in commands:
            if cmd.risk_level == RiskLevel.DESTRUCTIVE:
                if 'reset' in cmd.args and '--hard' in cmd.args:
                    alternatives.append(GitCommand(
                        command="git",
                        args=["reset", "--soft", "HEAD~1"],
                        description="Safer option: Undo commit but keep changes",
                        risk_level=RiskLevel.MODERATE,
                        requires_confirmation=True
                    ))
        
        return alternatives if alternatives else None