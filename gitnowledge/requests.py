from typing import Any

import requests
from loguru import logger


def get_api_url(
    path: str, context_manager: "gitnowledge.contexts.GitnowledgeContextManager"
) -> str:
    logger.debug("Building URL for {}", path)
    context = context_manager.get()
    url = context.base_url
    if context.git_host == "github":
        url += "/repos/" + context.repo_slug + "/commits"
        url += (
            "?sha=" + context.branch + "&path=" + path + "&ref_name=" + context.branch
        )
    elif context.git_host == "gitlab":
        url += "/projects/" + context.gitlab_project_id + "/repository/commits"
        url += "?branch=" + context.branch + "&path=" + path
    logger.debug("URL: {}", url)
    return str(url)


def query_git_host_api(path: str, context_manager: "GitnowledgeContextManager") -> Any:
    r"""Get users who have contributed to specific file in the repository.

    Args:
        path: File with respect to repository root.
        context_manager: Options used for this project.
    """
    context = context_manager.get()
    url = get_api_url(path, context_manager)
    if context.git_host == "gitlab":
        auth_header = {"PRIVATE-TOKEN": context.token}
    elif context.token is None:
        # github without token
        auth_header = {}
    else:
        # GitHub with token
        auth_header = {"Authorization": "token " + context.token}
    res = requests.get(url=url, headers=auth_header, timeout=10)

    if res.status_code != 200:
        logger.warning(
            "Failed to get commit information. Status code: {}", res.status_code
        )
        return [{}]
    logger.debug("Request status: 200")
    return res.json()
