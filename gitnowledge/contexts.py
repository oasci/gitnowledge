from typing import Any

import os

from loguru import logger


# pylint: disable-next=too-many-instance-attributes
class GitnowledgeContextManager:
    r"""Contexts for setting up molecular simulations."""

    # pylint: disable-next=too-many-arguments, too-many-locals
    def __init__(
        self,
        enabled: bool = True,
        git_host: str = "github",
        repo_slug: str | None = None,
        gitlab_project_id: int | None = None,
        branch: str = "main",
        docs_path: str = "docs/",
        exclude: list[str] | None = None,
        cache_dir: str = ".cache/plugin/gitnowledge",
        token: str | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        self.enabled = enabled
        self.git_host = git_host.strip().lower()
        self.repo_slug = repo_slug
        self.gitlab_project_id = gitlab_project_id
        self.branch = branch
        self.docs_path = docs_path
        self.exclude = exclude
        if self.exclude is None:
            self.exclude = []
        self.cache_dir = cache_dir
        self.token = token
        if self.git_host == "github":
            self.base_url = f"https://api.github.com"
        elif self.git_host == "gitlab":
            self.base_url = f"https://gitlab.com/api/v4"

        self.update_attributes(kwargs)

    def update_attributes(self, attr_dict: dict[str, Any]) -> None:
        for key, value in attr_dict.items():
            setattr(self, key, value)

    def validate(self):
        if not self.enabled:
            logger.info("gitnowledge is disabled")
        if self.repo_slug is None:
            logger.error("repo_slug must be specified")
            return
        if self.git_host == "github":
            pass
        elif self.git_host == "gitlab":
            if self.gitlab_project_id is None:
                logger.error("gitlab_project_id must be specified")
                return
            if self.token is None:
                token = os.environ.get("GITNOWLEDGE_TOKEN")
                if token is None:
                    logger.error("$GITNOWLEDGE_TOKEN env variable must be set")
                    return
                self.token = token
        else:
            logger.error("{} is not a valid git_host", self.git_host)
            return

    def __enter__(self):
        return self

    def get(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass
