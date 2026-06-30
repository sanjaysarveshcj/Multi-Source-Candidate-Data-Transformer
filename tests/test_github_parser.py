# pyrefly: ignore [missing-import]
import pytest
from unittest.mock import patch, MagicMock

from app.sources.github_parser import GitHubURLParser


class TestGitHubURLParser:

    def setup_method(self):
        self.parser = GitHubURLParser()

    ####################################################
    # Username extraction
    ####################################################

    def test_extract_username_from_full_url(self):
        username = self.parser._extract_username(
            "https://github.com/torvalds"
        )
        assert username == "torvalds"

    def test_extract_username_from_url_without_https(self):
        username = self.parser._extract_username(
            "github.com/octocat"
        )
        assert username == "octocat"

    def test_extract_username_from_plain_string(self):
        username = self.parser._extract_username(
            "sanjaysarvesh"
        )
        assert username == "sanjaysarvesh"

    def test_extract_username_strips_trailing_slash(self):
        username = self.parser._extract_username(
            "https://github.com/johndoe/"
        )
        assert username == "johndoe"

    ####################################################
    # Extract skills from repos
    ####################################################

    def test_extract_skills_from_repos(self):

        repos = [
            {"language": "Python", "topics": ["fastapi", "rest"]},
            {"language": "JavaScript", "topics": []},
            {"language": "Python", "topics": ["docker"]},
        ]

        skills = self.parser._extract_skills_from_repos(repos)

        assert "Python" in skills
        assert "JavaScript" in skills
        assert "Fastapi" in skills
        assert "Docker" in skills

    def test_extract_skills_empty_repos(self):

        skills = self.parser._extract_skills_from_repos([])
        assert skills == []

    ####################################################
    # Extract projects from repos
    ####################################################

    def test_extract_projects_skips_forks(self):

        repos = [
            {
                "fork": True,
                "name": "forked-repo",
                "description": "A fork",
                "created_at": "2024-01-01T00:00:00Z",
                "pushed_at": "2024-06-01T00:00:00Z",
            },
            {
                "fork": False,
                "name": "my-project",
                "description": "My original project",
                "created_at": "2023-01-01T00:00:00Z",
                "pushed_at": "2024-05-01T00:00:00Z",
            },
        ]

        projects = self.parser._extract_projects(repos)

        assert len(projects) == 1
        assert projects[0]["title"] == "my-project"

    ####################################################
    # Full parse with mocked API
    ####################################################

    @patch.object(GitHubURLParser, "_fetch_repos")
    @patch.object(GitHubURLParser, "_fetch_user")
    def test_parse_full(self, mock_user, mock_repos):

        mock_user.return_value = {
            "name": "Linus Torvalds",
            "login": "torvalds",
            "email": "torvalds@linux.org",
            "bio": "Creator of Linux",
            "location": "Portland, OR",
            "blog": "https://torvalds.dev",
            "html_url": "https://github.com/torvalds",
        }

        mock_repos.return_value = [
            {
                "name": "linux",
                "language": "C",
                "topics": ["kernel", "os"],
                "fork": False,
                "description": "Linux kernel source",
                "created_at": "2011-01-01T00:00:00Z",
                "pushed_at": "2024-06-01T00:00:00Z",
            },
        ]

        result = self.parser.parse(
            "https://github.com/torvalds"
        )

        assert result.source == "GitHub"
        assert result.full_name == "Linus Torvalds"
        assert "torvalds@linux.org" in result.emails
        assert result.headline == "Creator of Linux"
        assert result.location == {"city": "Portland", "region": "OR"}
        assert "C" in result.skills
        assert len(result.experience) == 0
