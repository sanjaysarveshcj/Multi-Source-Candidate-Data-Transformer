import requests
import re
from typing import List

from app.models.raw_candidate import RawCandidate
from app.sources.parser import SourceParser
from app.logging.logger import logger


class GitHubURLParser(SourceParser):
    """
    Parses a GitHub profile URL and fetches candidate data
    from the GitHub public API.

    Accepts either:
        - A full URL string: "https://github.com/username"
        - A plain username: "username"
    """

    GITHUB_API = "https://api.github.com"

    GITHUB_URL_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_-]+)"
    )

    ########################################################
    # Extract username from URL or plain string
    ########################################################

    def _extract_username(self, source: str) -> str:

        match = self.GITHUB_URL_PATTERN.search(source.strip())

        if match:
            return match.group(1)

        # Treat as plain username
        return source.strip().rstrip("/")

    ########################################################
    # Fetch user profile from GitHub API
    ########################################################

    def _fetch_user(self, username: str) -> dict:

        url = f"{self.GITHUB_API}/users/{username}"

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        return response.json()

    ########################################################
    # Fetch public repos from GitHub API
    ########################################################

    def _fetch_repos(self, username: str) -> list:

        url = f"{self.GITHUB_API}/users/{username}/repos"

        params = {
            "sort": "updated",
            "per_page": 30,
            "type": "owner",
        }

        response = requests.get(
            url, params=params, timeout=10
        )

        response.raise_for_status()

        return response.json()

    ########################################################
    # Extract programming languages / skills from repos
    ########################################################

    def _extract_skills_from_repos(self, repos: list) -> list:

        languages = set()

        topics = set()

        for repo in repos:

            if repo.get("language"):
                languages.add(repo["language"])

            for topic in repo.get("topics", []):
                topics.add(topic.title())

        return sorted(languages | topics)

    ########################################################
    # Build experience from notable repos
    ########################################################

    def _extract_projects(self, repos: list) -> list:

        projects = []

        for repo in repos:

            if repo.get("fork"):
                continue

            # Convert full dates to YYYY-MM format
            start_raw = repo.get("created_at", "")
            end_raw = repo.get("pushed_at", "")

            projects.append({
                "company": "GitHub (Open Source)",
                "title": repo.get("name", ""),
                "summary": repo.get("description") or "",
                "start": start_raw[:7] if start_raw else "",
                "end": end_raw[:7] if end_raw else "",
            })

        return projects[:10]  # Limit to top 10

    ########################################################
    # Main parse method
    ########################################################

    def parse(self, source_path: str) -> List[RawCandidate]:

        username = self._extract_username(source_path)

        logger.info(
            f"Fetching GitHub profile for: {username}"
        )

        user = self._fetch_user(username)
        repos = self._fetch_repos(username)

        ####################################################
        # Extract candidate fields
        ####################################################

        full_name = (
            user.get("name")
            or user.get("login")
        )

        email = user.get("email")

        headline = user.get("bio") or ""

        raw_location = user.get("location") or ""

        # Parse location string into structured dict
        location = {}
        if raw_location:
            parts = [p.strip() for p in raw_location.split(",")]
            if len(parts) >= 1:
                location["city"] = parts[0]
            if len(parts) >= 2:
                location["region"] = parts[1]
            if len(parts) >= 3:
                location["country"] = parts[2]

        blog = user.get("blog") or ""

        profile_url = user.get("html_url", "")

        # Build structured links dict
        other_links = []
        if blog:
            other_links.append(blog)

        links = {
            "linkedin": None,
            "github": profile_url or None,
            "portfolio": None,
            "other": other_links,
        }

        skills = self._extract_skills_from_repos(repos)

        # Do not include GitHub projects as professional experience
        experience = []

        logger.info(
            f"GitHub profile parsed: {full_name} "
            f"({len(skills)} skills)"
        )

        return [RawCandidate(
            source="GitHub",
            full_name=full_name,
            headline=headline,
            location=location,
            emails=[] if not email else [email],
            phones=[],
            skills=skills,
            experience=experience,
            education=[],
            links=links,
        )]