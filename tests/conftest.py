import os
import tempfile

import pytest

from gitnowledge import enable_logging
from gitnowledge.contexts import GitnowledgeContextManager

TEST_DIR = os.path.dirname(__file__)


@pytest.fixture(scope="session", autouse=True)
def turn_on_logging():
    enable_logging(10)


@pytest.fixture
def gitkeep_path():
    return "tests/files/.gitkeep"


@pytest.fixture
def gitnowledge_gitlab_context():
    tempdir = tempfile.TemporaryDirectory()
    context_manager = GitnowledgeContextManager(
        enabled=True,
        git_host="gitlab",
        repo_slug="oasci/software/gitnowledge",
        gitlab_project_id="52388375",
        branch="main",
        docs_path="docs/",
        cache_dir=tempdir.name,
    )
    return context_manager
