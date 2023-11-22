from gitnowledge.requests import query_git_host_api


def test_gitlab_api_request(gitkeep_path, gitnowledge_gitlab_context):
    res = query_git_host_api(gitkeep_path, gitnowledge_gitlab_context)
    assert len(res) == 3


def test_github_api_request(gitkeep_path, gitnowledge_github_context):
    res = query_git_host_api(gitkeep_path, gitnowledge_github_context)
    assert len(res) == 3
