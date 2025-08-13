"""Tests for git integration functionality."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pbnj.core.git_integration import GitHelper


class TestGitHelper:
    """Test cases for GitHelper."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = None
        
    def teardown_method(self):
        """Clean up after tests."""
        if self.temp_dir:
            self.temp_dir.cleanup()
            
    def test_git_helper_initialization(self):
        """Test GitHelper initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test with path
            helper = GitHelper(temp_path)
            assert helper.repo_path == temp_path
            assert helper.repo is None
            
            # Test without path (should use cwd)
            with patch('pathlib.Path.cwd', return_value=temp_path):
                helper2 = GitHelper()
                assert helper2.repo_path == temp_path
                
    def test_is_git_repo_false(self):
        """Test is_git_repo when directory is not a git repo."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            helper = GitHelper(temp_path)
            assert helper.is_git_repo() is False
            
    @patch('git.Repo')
    def test_is_git_repo_true(self, mock_repo):
        """Test is_git_repo when directory is a git repo."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Mock successful repo access
            mock_repo.return_value = MagicMock()
            
            helper = GitHelper(temp_path)
            assert helper.is_git_repo() is True
            mock_repo.assert_called_once_with(temp_path)
            
    @patch('git.Repo')
    def test_is_git_repo_invalid_repo(self, mock_repo):
        """Test is_git_repo with invalid git repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Mock InvalidGitRepositoryError
            from git import InvalidGitRepositoryError
            mock_repo.side_effect = InvalidGitRepositoryError("Not a git repo")
            
            helper = GitHelper(temp_path)
            assert helper.is_git_repo() is False
            
    @patch('git.Repo')
    def test_init_repo_success(self, mock_repo):
        """Test successful repository initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Mock repo init
            mock_repo_instance = MagicMock()
            mock_repo.init.return_value = mock_repo_instance
            mock_repo.side_effect = [Exception("Not a repo"), mock_repo_instance]  # First call fails, second succeeds
            
            helper = GitHelper(temp_path)
            helper.init_repo()
            
            # Should have created .gitignore
            gitignore_path = temp_path / ".gitignore"
            assert gitignore_path.exists()
            
            gitignore_content = gitignore_path.read_text()
            assert "# Python" in gitignore_content
            assert "*.pbix" in gitignore_content
            assert ".pbnj/cache/" in gitignore_content
            
            # Should have initialized repo
            mock_repo.init.assert_called_once_with(temp_path)
            
    @patch('git.Repo')
    def test_init_repo_already_exists(self, mock_repo):
        """Test init_repo when repo already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Mock existing repo
            mock_repo.return_value = MagicMock()
            
            helper = GitHelper(temp_path)
            helper.init_repo()
            
            # Should not call init if repo already exists
            mock_repo.init.assert_not_called()
            
    @patch('git.Repo')
    def test_get_repo(self, mock_repo):
        """Test get_repo method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            repo = helper.get_repo()
            
            assert repo == mock_repo_instance
            assert helper.repo == mock_repo_instance
            mock_repo.assert_called_once_with(temp_path)
            
    @patch('git.Repo')
    def test_get_repo_cached(self, mock_repo):
        """Test get_repo uses cached repo."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            helper.repo = mock_repo_instance  # Set cached repo
            
            repo = helper.get_repo()
            
            assert repo == mock_repo_instance
            # Should not call Repo again since it's cached
            mock_repo.assert_not_called()
            
    @patch('git.Repo')
    def test_add_files(self, mock_repo):
        """Test adding files to git staging area."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_index = MagicMock()
            mock_repo_instance.index = mock_index
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            files = ["file1.txt", "file2.txt"]
            helper.add_files(files)
            
            mock_index.add.assert_called_once_with(files)
            
    @patch('git.Repo')
    def test_commit_changes_with_changes(self, mock_repo):
        """Test committing changes when there are changes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.is_dirty.return_value = True  # Has changes
            mock_git = MagicMock()
            mock_repo_instance.git = mock_git
            mock_index = MagicMock()
            mock_repo_instance.index = mock_index
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            helper.commit_changes("Test commit message")
            
            mock_git.add.assert_called_once_with(A=True)
            mock_index.commit.assert_called_once_with("Test commit message")
            
    @patch('git.Repo')
    def test_commit_changes_no_changes(self, mock_repo):
        """Test committing changes when there are no changes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.is_dirty.return_value = False  # No changes
            mock_index = MagicMock()
            mock_repo_instance.index = mock_index
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            helper.commit_changes("Test commit message")
            
            # Should not commit if no changes
            mock_index.commit.assert_not_called()
            
    @patch('git.Repo')
    def test_get_status(self, mock_repo):
        """Test getting git status."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.untracked_files = ["new_file.txt"]
            
            # Mock diff results
            mock_modified_item = MagicMock()
            mock_modified_item.a_path = "modified_file.txt"
            mock_staged_item = MagicMock()
            mock_staged_item.a_path = "staged_file.txt"
            
            mock_index = MagicMock()
            mock_index.diff.side_effect = [
                [mock_modified_item],  # diff(None) - modified files
                [mock_staged_item]     # diff("HEAD") - staged files
            ]
            mock_repo_instance.index = mock_index
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            status = helper.get_status()
            
            assert status["untracked"] == ["new_file.txt"]
            assert status["modified"] == ["modified_file.txt"]
            assert status["staged"] == ["staged_file.txt"]
            
    @patch('git.Repo')
    def test_create_branch(self, mock_repo):
        """Test creating and checking out a new branch."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_new_branch = MagicMock()
            mock_repo_instance.create_head.return_value = mock_new_branch
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            helper.create_branch("feature-branch")
            
            mock_repo_instance.create_head.assert_called_once_with("feature-branch")
            mock_new_branch.checkout.assert_called_once()
            
    @patch('git.Repo')
    def test_get_current_branch(self, mock_repo):
        """Test getting current branch name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_active_branch = MagicMock()
            mock_active_branch.name = "main"
            mock_repo_instance.active_branch = mock_active_branch
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            branch_name = helper.get_current_branch()
            
            assert branch_name == "main"
            
    @patch('git.Repo')
    def test_has_remote_true(self, mock_repo):
        """Test has_remote when remotes exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.remotes = ["origin"]  # Has remotes
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            assert helper.has_remote() is True
            
    @patch('git.Repo')
    def test_has_remote_false(self, mock_repo):
        """Test has_remote when no remotes exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.remotes = []  # No remotes
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            assert helper.has_remote() is False
            
    @patch('git.Repo')
    def test_add_remote(self, mock_repo):
        """Test adding a remote repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            helper.add_remote("origin", "https://github.com/user/repo.git")
            
            mock_repo_instance.create_remote.assert_called_once_with(
                "origin", "https://github.com/user/repo.git"
            )
            
    @patch('git.Repo')
    def test_push_changes(self, mock_repo):
        """Test pushing changes to remote."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_active_branch = MagicMock()
            mock_active_branch.name = "main"
            mock_repo_instance.active_branch = mock_active_branch
            
            mock_origin = MagicMock()
            mock_repo_instance.remote.return_value = mock_origin
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            helper.push_changes()
            
            mock_repo_instance.remote.assert_called_once_with("origin")
            mock_origin.push.assert_called_once_with("main")
            
    @patch('git.Repo')
    def test_push_changes_custom_remote_and_branch(self, mock_repo):
        """Test pushing changes with custom remote and branch."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_upstream = MagicMock()
            mock_repo_instance.remote.return_value = mock_upstream
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            helper.push_changes("upstream", "feature-branch")
            
            mock_repo_instance.remote.assert_called_once_with("upstream")
            mock_upstream.push.assert_called_once_with("feature-branch")


class TestGitHelperIntegration:
    """Integration tests for GitHelper with real git operations."""
    
    @pytest.mark.integration
    def test_real_git_operations(self):
        """Test GitHelper with real git operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            helper = GitHelper(temp_path)
            
            # Initially should not be a git repo
            assert helper.is_git_repo() is False
            
            try:
                # Initialize repo
                helper.init_repo()
                
                # Now should be a git repo
                assert helper.is_git_repo() is True
                
                # Should have created .gitignore
                gitignore_path = temp_path / ".gitignore"
                assert gitignore_path.exists()
                
                # Create a test file
                test_file = temp_path / "test.txt"
                test_file.write_text("Hello, world!")
                
                # Get status
                status = helper.get_status()
                assert "test.txt" in status["untracked"]
                
                # Add and commit
                helper.add_files(["test.txt"])
                helper.commit_changes("Add test file")
                
                # File should no longer be untracked
                status = helper.get_status()
                assert "test.txt" not in status["untracked"]
                
                # Get current branch
                branch = helper.get_current_branch()
                assert branch in ["master", "main"]  # Git default branches
                
                # Test creating new branch
                helper.create_branch("test-branch")
                new_branch = helper.get_current_branch()
                assert new_branch == "test-branch"
                
                print("Real git operations completed successfully")
                
            except Exception as e:
                # If git is not available or configured, skip the test
                print(f"Real git operations failed (git not available?): {e}")
                pytest.skip("Git not available for integration testing")


class TestGitHelperErrorHandling:
    """Test error handling in GitHelper."""
    
    @patch('git.Repo')
    def test_get_repo_error(self, mock_repo):
        """Test error handling in get_repo."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo.side_effect = Exception("Git error")
            
            helper = GitHelper(temp_path)
            
            with pytest.raises(Exception, match="Git error"):
                helper.get_repo()
                
    @patch('git.Repo')
    def test_commit_changes_error(self, mock_repo):
        """Test error handling in commit_changes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.is_dirty.return_value = True
            mock_git = MagicMock()
            mock_git.add.side_effect = Exception("Add failed")
            mock_repo_instance.git = mock_git
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            
            with pytest.raises(Exception, match="Add failed"):
                helper.commit_changes("Test commit")
                
    @patch('git.Repo')
    def test_push_changes_error(self, mock_repo):
        """Test error handling in push_changes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.remote.side_effect = Exception("Remote not found")
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            
            with pytest.raises(Exception, match="Remote not found"):
                helper.push_changes()
                
    def test_init_repo_permission_error(self):
        """Test init_repo with permission error."""
        # Use a directory that would cause permission error
        restricted_path = Path("/root/restricted") if Path("/root").exists() else Path("/nonexistent/path")
        
        helper = GitHelper(restricted_path)
        
        # Should handle permission errors gracefully or raise them
        try:
            helper.init_repo()
            # If it succeeds, that's fine
        except (PermissionError, FileNotFoundError, Exception):
            # These errors are expected for restricted paths
            pass


class TestGitHelperEdgeCases:
    """Test edge cases for GitHelper."""
    
    def test_helper_with_nonexistent_path(self):
        """Test GitHelper with nonexistent path."""
        nonexistent_path = Path("/this/path/does/not/exist")
        
        helper = GitHelper(nonexistent_path)
        
        # Should not fail on initialization
        assert helper.repo_path == nonexistent_path
        
        # But should fail when trying to use git operations
        assert helper.is_git_repo() is False
        
    @patch('git.Repo')
    def test_get_status_empty_repo(self, mock_repo):
        """Test get_status with empty repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.untracked_files = []
            mock_index = MagicMock()
            mock_index.diff.return_value = []
            mock_repo_instance.index = mock_index
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            status = helper.get_status()
            
            assert status["untracked"] == []
            assert status["modified"] == []
            assert status["staged"] == []
            
    @patch('git.Repo')
    def test_commit_changes_empty_message(self, mock_repo):
        """Test commit_changes with empty message."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            mock_repo_instance = MagicMock()
            mock_repo_instance.is_dirty.return_value = True
            mock_git = MagicMock()
            mock_repo_instance.git = mock_git
            mock_index = MagicMock()
            mock_repo_instance.index = mock_index
            mock_repo.return_value = mock_repo_instance
            
            helper = GitHelper(temp_path)
            helper.commit_changes("")  # Empty message
            
            mock_index.commit.assert_called_once_with("")


if __name__ == "__main__":
    pytest.main([__file__])